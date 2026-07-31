"""
RBAC Synchronization Service for PawMatch.
Synchronizes declarative Role & Permission definitions with Django Groups and Permissions.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Set

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from apps.accounts.constants import AuditAction
from apps.accounts.permissions import PermissionName
from apps.accounts.role_permissions import ROLE_PERMISSIONS_MAP
from apps.accounts.roles import RoleName
from apps.audit_logs.services.audit_service import AuditService

logger = logging.getLogger("apps.accounts")

# Declarative Role -> Django Group display name mapping
ROLE_TO_GROUP_NAME: Dict[str, str] = {
    RoleName.ADMINISTRATOR: "Administrator",
    RoleName.SHELTER_MANAGER: "Shelter Manager",
    RoleName.SHELTER_STAFF: "Shelter Staff",
    RoleName.VETERINARIAN: "Veterinarian",
    RoleName.VOLUNTEER: "Volunteer",
    RoleName.ADOPTER: "Adopter",
}


class RBACService:
    """
    Domain service providing idempotent, transaction-safe synchronization of
    declarative RBAC roles and permissions with Django's native Group & Permission models.
    """

    @classmethod
    def get_group_name_for_role(cls, role_name: str) -> str:
        """Returns Django Group display name for a given platform role string."""
        return ROLE_TO_GROUP_NAME.get(role_name, role_name.replace("_", " ").title())

    @classmethod
    def sync_permissions(cls) -> Dict[str, Permission]:
        """
        Ensures all permissions in PermissionName registry exist in Django Permission table.
        Returns dictionary mapping permission strings (e.g. 'pets.view') to Permission instances.
        """
        all_perm_strings: Set[str] = PermissionName.get_all_permissions()
        permission_map: Dict[str, Permission] = {}

        for perm_str in sorted(all_perm_strings):
            if "." in perm_str:
                app_label, codename = perm_str.split(".", 1)
            else:
                app_label, codename = "accounts", perm_str

            # Find or create a ContentType for the specified app_label
            ct = ContentType.objects.filter(app_label=app_label).first()
            if not ct:
                ct, _ = ContentType.objects.get_or_create(
                    app_label=app_label,
                    model=app_label,
                )

            formatted_action = codename.replace("_", " ").replace(".", " ")
            name = f"Can {formatted_action} {app_label}"

            perm_obj, _ = Permission.objects.get_or_create(
                content_type=ct,
                codename=codename,
                defaults={"name": name},
            )
            permission_map[perm_str] = perm_obj

        return permission_map

    @classmethod
    def sync_groups_and_mappings(
        cls, permission_map: Dict[str, Permission]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Synchronizes Django Groups and Group -> Permission mappings.
        Cleans up stale mappings automatically if permissions are removed from code definitions.
        """
        summary: Dict[str, Dict[str, Any]] = {}

        for role_name, group_display_name in ROLE_TO_GROUP_NAME.items():
            # Never duplicate groups; fetch or create cleanly
            group_qs = Group.objects.filter(name=group_display_name)
            if group_qs.exists():
                group = group_qs.first()
            else:
                group = Group.objects.create(name=group_display_name)

            target_perm_strings = ROLE_PERMISSIONS_MAP.get(role_name, set())
            target_perm_objs = [
                permission_map[p_str]
                for p_str in target_perm_strings
                if p_str in permission_map
            ]

            # Set exact permissions for the group (idempotent, replaces/cleans stale perms)
            group.permissions.set(target_perm_objs)

            summary[group_display_name] = {
                "role_name": role_name,
                "group_id": group.id,
                "group_name": group_display_name,
                "permission_count": len(target_perm_objs),
                "permissions": sorted(list(target_perm_strings)),
            }

        return summary

    @classmethod
    def sync(cls) -> Dict[str, Any]:
        """
        Main synchronization entrypoint.
        Executes idempotent, transaction-safe synchronization of all roles, permissions,
        and group-permission mappings.
        """
        start_time = datetime.now(timezone.utc)
        logger.info(
            "RBAC_SYNC_STARTED",
            extra={"timestamp": start_time.isoformat()},
        )
        AuditService.log_event(
            action=AuditAction.RBAC_SYNC_STARTED,
            status="SUCCESS",
            details={"started_at": start_time.isoformat()},
        )

        try:
            with transaction.atomic():
                permission_map = cls.sync_permissions()
                role_summary = cls.sync_groups_and_mappings(permission_map)

            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()

            result = {
                "status": "SUCCESS",
                "timestamp": end_time.isoformat(),
                "duration_seconds": round(duration, 4),
                "roles_synchronized": len(role_summary),
                "permissions_synchronized": len(permission_map),
                "roles": role_summary,
            }

            logger.info(
                f"RBAC_SYNC_COMPLETED duration={duration:.4f}s roles={len(role_summary)} perms={len(permission_map)}",
                extra=result,
            )
            AuditService.log_event(
                action=AuditAction.RBAC_SYNC_COMPLETED,
                status="SUCCESS",
                details={
                    "duration_seconds": round(duration, 4),
                    "roles_synchronized": len(role_summary),
                    "permissions_synchronized": len(permission_map),
                },
            )
            return result

        except Exception as exc:
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()

            error_msg = str(exc)
            logger.error(
                f"RBAC_SYNC_FAILED error={error_msg}",
                extra={
                    "timestamp": end_time.isoformat(),
                    "duration_seconds": round(duration, 4),
                    "error": error_msg,
                },
            )
            AuditService.log_event(
                action=AuditAction.RBAC_SYNC_FAILED,
                status="FAILED",
                details={
                    "duration_seconds": round(duration, 4),
                    "error": error_msg,
                },
            )
            raise

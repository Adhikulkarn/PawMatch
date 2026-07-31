"""
Role Management Service for PawMatch.
Encapsulates role assignment, removal, replacement, and permission queries
while maintaining synchronization with Django Groups.
"""

import logging
from typing import Any, Iterable, Optional, Set

from django.contrib.auth.models import Group
from django.db import transaction

from apps.accounts.config import accounts_config
from apps.accounts.constants import AuditAction
from apps.accounts.events import EventDispatcher
from apps.accounts.exceptions import (
    DuplicateRoleException,
    InvalidRoleException,
    RoleNotAssignedException,
)
from apps.accounts.permissions import PermissionName
from apps.accounts.role_permissions import get_permissions_for_role
from apps.accounts.roles import RoleName
from apps.accounts.services.rbac_service import ROLE_TO_GROUP_NAME, RBACService
from apps.audit_logs.services.audit_service import AuditService

logger = logging.getLogger("apps.accounts")

# Reverse mapping from Django Group name -> RoleName constant
GROUP_NAME_TO_ROLE: dict = {v: k for k, v in ROLE_TO_GROUP_NAME.items()}


class RoleService:
    """
    Service layer executing user role assignments, removals, replacements, and role-permission queries.
    Encapsulates Django Group synchronization under the hood.
    """

    @classmethod
    def _validate_role(cls, role_name: str) -> str:
        """Validates that a role string matches a defined platform RoleName."""
        if not role_name or not isinstance(role_name, str):
            raise InvalidRoleException("Invalid role specified.")

        normalized = role_name.strip().upper()
        if normalized not in RoleName.get_all_roles():
            raise InvalidRoleException(
                f"Role '{role_name}' does not exist in platform role registry."
            )
        return normalized

    @classmethod
    def _get_group_for_role(cls, role_name: str) -> Group:
        """Retrieves or creates Django Group corresponding to role."""
        group_display_name = RBACService.get_group_name_for_role(role_name)
        group, _ = Group.objects.get_or_create(name=group_display_name)
        return group

    @classmethod
    def invalidate_user_permission_cache(cls, user: Any) -> None:
        """Invalidates in-memory cached roles and permissions for user on authorization updates."""
        if user is not None:
            for attr in (
                "_rbac_roles_cache",
                "_rbac_perms_cache",
                "_group_perm_cache",
                "_perm_cache",
            ):
                if hasattr(user, attr):
                    delattr(user, attr)

    @classmethod
    def _update_user_role_field(cls, user: Any, role_name: str) -> None:
        """Safely updates user.role model field if it exists as a database column on model schema."""
        if hasattr(user, "_meta") and hasattr(user._meta, "fields"):
            field_names = [f.name for f in user._meta.fields]
            if "role" in field_names:
                setattr(user, "role", role_name)
                update_fields = ["role"]
                if "updated_at" in field_names:
                    update_fields.append("updated_at")
                user.save(update_fields=update_fields)

    @classmethod
    def get_roles(cls, user: Any) -> Set[str]:
        """
        Returns set of platform RoleName string constants assigned to user.
        Utilizes request-level in-memory caching to avoid redundant queries.
        """
        if not user or not user.is_authenticated:
            return set()

        if hasattr(user, "_rbac_roles_cache"):
            return getattr(user, "_rbac_roles_cache")

        roles: Set[str] = set()

        # 1. Inspect user.groups if present on object
        if hasattr(user, "groups"):
            try:
                for group in user.groups.all():
                    if group.name in GROUP_NAME_TO_ROLE:
                        roles.add(GROUP_NAME_TO_ROLE[group.name])
                    else:
                        normalized = group.name.upper().replace(" ", "_")
                        if normalized in RoleName.get_all_roles():
                            roles.add(normalized)
            except Exception:
                pass

        # 2. Inspect user.role property/attribute if populated
        if hasattr(user, "role") and getattr(user, "role"):
            normalized_user_role = str(user.role).strip().upper()
            if normalized_user_role in RoleName.get_all_roles():
                roles.add(normalized_user_role)

        # 3. Staff fallback if no other role explicitly assigned
        if getattr(user, "is_staff", False) and not roles:
            roles.add(RoleName.SHELTER_STAFF)

        # 4. Superuser override
        if getattr(user, "is_superuser", False):
            roles.add(RoleName.ADMINISTRATOR)

        # 5. Default role fallback if no explicit role/group assigned
        if not roles:
            roles.add(accounts_config.default_role)

        if hasattr(user, "__dict__"):
            setattr(user, "_rbac_roles_cache", roles)

        return roles

    @classmethod
    def has_role(cls, user: Any, role: str) -> bool:
        """
        Checks if user possesses the specified platform role.
        """
        if not user or not user.is_authenticated:
            return False

        normalized_role = cls._validate_role(role)

        if (
            getattr(user, "is_superuser", False)
            and normalized_role == RoleName.ADMINISTRATOR
        ):
            return True

        user_roles = cls.get_roles(user)
        return normalized_role in user_roles

    @classmethod
    def get_permissions(cls, user: Any) -> Set[str]:
        """
        Returns set of all permission strings assigned to user across all roles and permissions.
        Utilizes request-level in-memory caching to optimize resolution.
        """
        if not user or not user.is_authenticated:
            return set()

        if hasattr(user, "_rbac_perms_cache"):
            return getattr(user, "_rbac_perms_cache")

        if getattr(user, "is_superuser", False):
            all_perms = PermissionName.get_all_permissions()
            if hasattr(user, "__dict__"):
                setattr(user, "_rbac_perms_cache", all_perms)
            return all_perms

        permissions: Set[str] = set()

        # Permissions from assigned roles
        user_roles = cls.get_roles(user)
        for role_name in user_roles:
            permissions.update(get_permissions_for_role(role_name))

        # Permissions from Django user_permissions or groups.permissions
        if hasattr(user, "get_all_permissions"):
            for perm_str in user.get_all_permissions():
                permissions.add(perm_str)

        if hasattr(user, "__dict__"):
            setattr(user, "_rbac_perms_cache", permissions)

        return permissions

    @classmethod
    def assign_role(
        cls,
        user: Any,
        role: str,
        actor: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> Any:
        """
        Assigns a role to a user.
        Raises InvalidRoleException if role is invalid.
        Raises DuplicateRoleException if user already has role assigned.
        """
        normalized_role = cls._validate_role(role)
        group = cls._get_group_for_role(normalized_role)

        if hasattr(user, "groups") and user.groups.filter(id=group.id).exists():
            raise DuplicateRoleException(
                f"User {user.email} already has role '{normalized_role}' assigned."
            )

        with transaction.atomic():
            user.groups.add(group)

            cls._update_user_role_field(user, normalized_role)
            cls.invalidate_user_permission_cache(user)

            actor_id = getattr(actor, "id", None) if actor else None
            EventDispatcher.dispatch_role_assigned(
                user_id=user.id,
                email=user.email,
                role_name=normalized_role,
                assigned_by=actor_id,
                request=request,
            )

            AuditService.log_event(
                action=AuditAction.ROLE_ASSIGNED,
                request=request,
                user_id=user.id,
                email=user.email,
                status="SUCCESS",
                details={
                    "role": normalized_role,
                    "assigned_by": str(actor_id) if actor_id else None,
                },
            )

        return user

    @classmethod
    def remove_role(
        cls,
        user: Any,
        role: str,
        actor: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> Any:
        """
        Removes a role from a user.
        Raises InvalidRoleException if role is invalid.
        Raises RoleNotAssignedException if user does not possess role.
        """
        normalized_role = cls._validate_role(role)

        if not cls.has_role(user, normalized_role):
            raise RoleNotAssignedException(
                f"Role '{normalized_role}' is not assigned to user {user.email}."
            )

        with transaction.atomic():
            group_name = RBACService.get_group_name_for_role(normalized_role)
            groups = user.groups.filter(name=group_name)
            if groups.exists():
                user.groups.remove(*groups)

            cls.invalidate_user_permission_cache(user)
            remaining_roles = cls.get_roles(user) - {normalized_role}
            new_primary = next(iter(remaining_roles), RoleName.ADOPTER)
            cls._update_user_role_field(user, new_primary)

            actor_id = getattr(actor, "id", None) if actor else None
            EventDispatcher.dispatch_role_removed(
                user_id=user.id,
                email=user.email,
                role_name=normalized_role,
                removed_by=actor_id,
                request=request,
            )

            AuditService.log_event(
                action=AuditAction.ROLE_REMOVED,
                request=request,
                user_id=user.id,
                email=user.email,
                status="SUCCESS",
                details={
                    "role": normalized_role,
                    "removed_by": str(actor_id) if actor_id else None,
                },
            )

        return user

    @classmethod
    def replace_roles(
        cls,
        user: Any,
        roles: Iterable[str],
        actor: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> Any:
        """
        Replaces all user roles with a new set of roles.
        Raises InvalidRoleException if any role is invalid.
        """
        normalized_roles = {cls._validate_role(r) for r in roles}

        with transaction.atomic():
            target_groups = [cls._get_group_for_role(r) for r in normalized_roles]
            user.groups.set(target_groups)

            cls.invalidate_user_permission_cache(user)
            primary_role = next(iter(normalized_roles), RoleName.ADOPTER)
            cls._update_user_role_field(user, primary_role)

            actor_id = getattr(actor, "id", None) if actor else None
            EventDispatcher.dispatch_role_replaced(
                user_id=user.id,
                email=user.email,
                roles=sorted(list(normalized_roles)),
                replaced_by=actor_id,
                request=request,
            )

            AuditService.log_event(
                action=AuditAction.ROLE_REPLACED,
                request=request,
                user_id=user.id,
                email=user.email,
                status="SUCCESS",
                details={
                    "roles": sorted(list(normalized_roles)),
                    "replaced_by": str(actor_id) if actor_id else None,
                },
            )

        return user

    @classmethod
    def clear_roles(
        cls,
        user: Any,
        actor: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> Any:
        """
        Removes all roles from a user.
        """
        return cls.replace_roles(user=user, roles=[], actor=actor, request=request)

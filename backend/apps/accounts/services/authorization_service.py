"""
Authorization domain service layer for PawMatch.
Encapsulates RBAC permission checking, role verification, policy engine evaluation,
and security audit logging.
"""

import logging
from typing import Any, Optional

from apps.accounts.config import accounts_config
from apps.accounts.constants import AuditAction, AuthMessage
from apps.accounts.events import EventDispatcher
from apps.accounts.exceptions import PermissionDeniedException
from apps.accounts.policies.policy_engine import PolicyEngine
from apps.accounts.role_permissions import get_permissions_for_role
from apps.accounts.roles import RoleName
from apps.audit_logs.services.audit_service import AuditService

logger = logging.getLogger("apps.accounts")


class AuthorizationService:
    """
    Domain service executing platform RBAC and policy-based authorization logic.
    """

    @classmethod
    def getUserRole(cls, user: Any) -> str:
        """Helper to get primary role of user, defaulting to accounts_config.default_role."""
        if not user or not user.is_authenticated:
            return ""
        if user.is_superuser:
            return RoleName.ADMINISTRATOR
        if hasattr(user, "role") and user.role:
            return str(user.role).upper()
        if user.is_staff:
            return RoleName.SHELTER_STAFF
        return accounts_config.default_role

    @classmethod
    def has_permission(cls, user: Any, permission: str) -> bool:
        """
        Checks if user has the requested permission through role mapping or superuser privilege.
        """
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        user_role = cls.getUserRole(user)
        role_permissions = get_permissions_for_role(user_role)

        if permission in role_permissions:
            return True

        if hasattr(user, "has_perm") and user.has_perm(permission):
            return True

        return False

    @classmethod
    def has_role(cls, user: Any, role_name: str) -> bool:
        """
        Checks if user possesses the specified platform role.
        """
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser and role_name.upper() == RoleName.ADMINISTRATOR:
            return True

        user_role = cls.getUserRole(user)
        return user_role.upper() == role_name.upper()

    @classmethod
    def can(cls, user: Any, action: str, resource: Optional[Any] = None) -> bool:
        """
        Evaluates policy-based authorization for user, action, and resource object.
        """
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if not accounts_config.enable_policy_engine:
            return True

        return PolicyEngine.evaluate(user=user, action=action, resource=resource)

    @classmethod
    def authorize(
        cls,
        user: Any,
        permission_or_action: str,
        resource: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> bool:
        """
        Main authorization entry point. Verifies permissions and policy engine rules,
        emitting security events and audit records.
        Raises PermissionDeniedException on failure.
        """
        if not user or not user.is_authenticated:
            AuditService.log_event(
                action=AuditAction.AUTHORIZATION_DENIED,
                request=request,
                status="FAILED",
                details={
                    "permission": permission_or_action,
                    "reason": "Unauthenticated user.",
                },
            )
            raise PermissionDeniedException(AuthMessage.PERMISSION_DENIED)

        # 1. Superuser override
        if user.is_superuser:
            EventDispatcher.dispatch_permission_granted(
                user_id=user.id,
                email=user.email,
                permission=permission_or_action,
                resource=resource,
                request=request,
            )
            AuditService.log_event(
                action=AuditAction.AUTHORIZATION_GRANTED,
                request=request,
                user_id=user.id,
                email=user.email,
                status="SUCCESS",
                details={"permission": permission_or_action},
            )
            return True

        # 2. Check RBAC permission or Policy Action
        authorized = False
        if resource is not None:
            authorized = cls.can(user, permission_or_action, resource)
        else:
            authorized = cls.has_permission(user, permission_or_action)

        if authorized:
            EventDispatcher.dispatch_permission_granted(
                user_id=user.id,
                email=user.email,
                permission=permission_or_action,
                resource=resource,
                request=request,
            )
            AuditService.log_event(
                action=AuditAction.AUTHORIZATION_GRANTED,
                request=request,
                user_id=user.id,
                email=user.email,
                status="SUCCESS",
                details={"permission": permission_or_action},
            )
            return True

        # Authorization failed
        EventDispatcher.dispatch_permission_denied(
            user_id=user.id,
            email=user.email,
            permission=permission_or_action,
            resource=resource,
            request=request,
        )

        AuditService.log_event(
            action=AuditAction.AUTHORIZATION_DENIED,
            request=request,
            user_id=user.id,
            email=user.email,
            status="FAILED",
            details={"permission": permission_or_action},
        )

        raise PermissionDeniedException(AuthMessage.PERMISSION_DENIED)

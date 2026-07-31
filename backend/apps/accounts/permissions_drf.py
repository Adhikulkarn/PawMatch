"""
DRF Permission classes for PawMatch Authorization Framework.
Provides declarative view and object-level permission enforcement.
"""

from typing import Any

from rest_framework.permissions import BasePermission

from apps.accounts.services.authorization_service import AuthorizationService


class HasPermission(BasePermission):
    """
    DRF permission class checking if authenticated user possesses a required permission string.
    Usage:
        class MyView(APIView):
            permission_classes = [HasPermission("pets.create")]
    """

    required_permission: str = ""

    def __init__(self, permission_name: str = ""):
        if permission_name:
            self.required_permission = permission_name

    def has_permission(self, request, view) -> bool:
        perm = (
            self.required_permission
            or getattr(view, "required_permission", "")
            or getattr(view, "permission_name", "")
        )
        if not perm:
            return True
        return AuthorizationService.has_permission(request.user, perm)


class HasRole(BasePermission):
    """
    DRF permission class checking if authenticated user possesses a required platform role.
    Usage:
        class AdminOnlyView(APIView):
            permission_classes = [HasRole("ADMINISTRATOR")]
    """

    required_role: str = ""

    def __init__(self, role_name: str = ""):
        if role_name:
            self.required_role = role_name

    def has_permission(self, request, view) -> bool:
        role = (
            self.required_role
            or getattr(view, "required_role", "")
            or getattr(view, "role_name", "")
        )
        if not role:
            return True
        return AuthorizationService.has_role(request.user, role)


class IsAdministratorRole(BasePermission):
    """
    DRF permission class restricting access exclusively to Administrators and Superusers.
    Usage:
        permission_classes = [IsAuthenticated, IsAdministratorRole]
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        from apps.accounts.roles import RoleName

        return AuthorizationService.has_role(request.user, RoleName.ADMINISTRATOR)


class HasObjectPermission(BasePermission):
    """
    DRF permission class evaluating object-level policy authorization.
    Usage:
        class DetailView(APIView):
            permission_classes = [HasObjectPermission("update")]
    """

    action_name: str = "view"

    def __init__(self, action: str = "view"):
        self.action_name = action

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj: Any) -> bool:
        action = getattr(view, "action_name", self.action_name)
        return AuthorizationService.can(request.user, action, obj)

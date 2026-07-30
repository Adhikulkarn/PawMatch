"""
Core infrastructure permission classes for PawMatch.
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Allows access only to superusers or platform staff members."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission allowing only owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, "owner", getattr(obj, "user", None))
        return owner == request.user


class IsShelterStaff(permissions.BasePermission):
    """Permission guard for shelter staff members."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        user_role = getattr(request.user, "role", None)
        return user_role in ["SHELTER_ADMIN", "SHELTER_STAFF"] or request.user.is_staff

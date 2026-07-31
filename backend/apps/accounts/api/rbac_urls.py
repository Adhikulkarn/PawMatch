"""
URL routing table for PawMatch RBAC (Role-Based Access Control) REST API endpoints.
"""

from django.urls import path

from apps.accounts.api.rbac_views import (
    AssignRoleAPIView,
    ClearRolesAPIView,
    RemoveRoleAPIView,
    ReplaceRolesAPIView,
    RoleDetailAPIView,
    RoleListAPIView,
    UserPermissionsAPIView,
    UserRolesAPIView,
)

app_name = "rbac"

urlpatterns = [
    path("roles/", RoleListAPIView.as_view(), name="role_list"),
    path("roles/<str:role>/", RoleDetailAPIView.as_view(), name="role_detail"),
    path("users/<uuid:id>/roles/", UserRolesAPIView.as_view(), name="user_roles"),
    path(
        "users/<uuid:id>/permissions/",
        UserPermissionsAPIView.as_view(),
        name="user_permissions",
    ),
    path(
        "users/<uuid:id>/assign-role/",
        AssignRoleAPIView.as_view(),
        name="assign_role",
    ),
    path(
        "users/<uuid:id>/remove-role/",
        RemoveRoleAPIView.as_view(),
        name="remove_role",
    ),
    path(
        "users/<uuid:id>/replace-roles/",
        ReplaceRolesAPIView.as_view(),
        name="replace_roles",
    ),
    path(
        "users/<uuid:id>/clear-roles/",
        ClearRolesAPIView.as_view(),
        name="clear_roles",
    ),
]

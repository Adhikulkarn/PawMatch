"""
API Views for PawMatch RBAC (Role-Based Access Control) Management subsystem.
Restricted exclusively to Administrator role holders and superusers.
"""

from typing import Any

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.api.rbac_serializers import (
    AssignRoleSerializer,
    RemoveRoleSerializer,
    ReplaceRolesSerializer,
    RoleDetailSerializer,
    UserPermissionsSerializer,
    UserRolesSerializer,
)
from apps.accounts.exceptions import InvalidRoleException
from apps.accounts.permissions_drf import IsAdministratorRole
from apps.accounts.role_permissions import get_permissions_for_role
from apps.accounts.roles import RoleName
from apps.accounts.services.rbac_service import RBACService
from apps.accounts.services.role_service import RoleService
from apps.core.responses import api_response

User = get_user_model()


class RoleListAPIView(APIView):
    """
    API endpoint listing all defined platform roles and their assigned permissions.
    """

    permission_classes = [IsAuthenticated, IsAdministratorRole]

    @extend_schema(
        tags=["RBAC Management"],
        summary="List platform roles",
        description="Retrieves a list of all platform roles, group names, and assigned permissions.",
        responses={200: RoleDetailSerializer(many=True)},
    )
    def get(self, request: Request) -> Response:
        all_roles = sorted(list(RoleName.get_all_roles()))
        roles_data = []

        for role_name in all_roles:
            group_name = RBACService.get_group_name_for_role(role_name)
            perms = sorted(list(get_permissions_for_role(role_name)))
            roles_data.append(
                {
                    "role": role_name,
                    "display_name": group_name,
                    "permission_count": len(perms),
                    "permissions": perms,
                }
            )

        return api_response(
            success=True,
            message="Platform roles retrieved successfully.",
            data=roles_data,
            status_code=status.HTTP_200_OK,
        )


class RoleDetailAPIView(APIView):
    """
    API endpoint retrieving details for a single platform role.
    """

    permission_classes = [IsAuthenticated, IsAdministratorRole]

    @extend_schema(
        tags=["RBAC Management"],
        summary="Get role detail",
        description="Retrieves details and permission mappings for a specified role string.",
        responses={200: RoleDetailSerializer},
    )
    def get(self, request: Request, role: str) -> Response:
        normalized_role = role.strip().upper()
        if normalized_role not in RoleName.get_all_roles():
            raise InvalidRoleException(f"Role '{role}' does not exist.")

        group_name = RBACService.get_group_name_for_role(normalized_role)
        perms = sorted(list(get_permissions_for_role(normalized_role)))

        role_data = {
            "role": normalized_role,
            "display_name": group_name,
            "permission_count": len(perms),
            "permissions": perms,
        }

        return api_response(
            success=True,
            message="Role details retrieved successfully.",
            data=role_data,
            status_code=status.HTTP_200_OK,
        )


class UserRolesAPIView(APIView):
    """
    API endpoint querying assigned roles for a specific user.
    """

    permission_classes = [IsAuthenticated, IsAdministratorRole]

    @extend_schema(
        tags=["RBAC Management"],
        summary="Get user roles",
        description="Retrieves all platform roles assigned to a user.",
        responses={200: UserRolesSerializer},
    )
    def get(self, request: Request, id: Any) -> Response:
        user = User.objects.filter(id=id).first()
        if not user:
            raise NotFound("User with specified ID does not exist.")

        user_roles = sorted(list(RoleService.get_roles(user)))
        return api_response(
            success=True,
            message="User roles retrieved successfully.",
            data={"user_id": str(user.id), "roles": user_roles},
            status_code=status.HTTP_200_OK,
        )


class UserPermissionsAPIView(APIView):
    """
    API endpoint querying aggregated permissions for a specific user.
    """

    permission_classes = [IsAuthenticated, IsAdministratorRole]

    @extend_schema(
        tags=["RBAC Management"],
        summary="Get user permissions",
        description="Retrieves all permissions assigned to a user across all roles.",
        responses={200: UserPermissionsSerializer},
    )
    def get(self, request: Request, id: Any) -> Response:
        user = User.objects.filter(id=id).first()
        if not user:
            raise NotFound("User with specified ID does not exist.")

        user_perms = sorted(list(RoleService.get_permissions(user)))
        return api_response(
            success=True,
            message="User permissions retrieved successfully.",
            data={"user_id": str(user.id), "permissions": user_perms},
            status_code=status.HTTP_200_OK,
        )


class AssignRoleAPIView(APIView):
    """
    API endpoint assigning a role to a user.
    """

    permission_classes = [IsAuthenticated, IsAdministratorRole]

    @extend_schema(
        tags=["RBAC Management"],
        summary="Assign role to user",
        description="Assigns a specified role to a user.",
        request=AssignRoleSerializer,
        responses={200: UserRolesSerializer},
    )
    def post(self, request: Request, id: Any) -> Response:
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(id=id).first()
        if not user:
            raise NotFound("User with specified ID does not exist.")

        role_name = serializer.validated_data["role"]
        RoleService.assign_role(
            user=user, role=role_name, actor=request.user, request=request
        )

        user_roles = sorted(list(RoleService.get_roles(user)))
        return api_response(
            success=True,
            message="Role assigned successfully.",
            data={"user_id": str(user.id), "roles": user_roles},
            status_code=status.HTTP_200_OK,
        )


class RemoveRoleAPIView(APIView):
    """
    API endpoint removing a role from a user.
    """

    permission_classes = [IsAuthenticated, IsAdministratorRole]

    @extend_schema(
        tags=["RBAC Management"],
        summary="Remove role from user",
        description="Removes a specified role from a user.",
        request=RemoveRoleSerializer,
        responses={200: UserRolesSerializer},
    )
    def post(self, request: Request, id: Any) -> Response:
        serializer = RemoveRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(id=id).first()
        if not user:
            raise NotFound("User with specified ID does not exist.")

        role_name = serializer.validated_data["role"]
        RoleService.remove_role(
            user=user, role=role_name, actor=request.user, request=request
        )

        user_roles = sorted(list(RoleService.get_roles(user)))
        return api_response(
            success=True,
            message="Role removed successfully.",
            data={"user_id": str(user.id), "roles": user_roles},
            status_code=status.HTTP_200_OK,
        )


class ReplaceRolesAPIView(APIView):
    """
    API endpoint replacing all roles assigned to a user.
    """

    permission_classes = [IsAuthenticated, IsAdministratorRole]

    @extend_schema(
        tags=["RBAC Management"],
        summary="Replace user roles",
        description="Replaces all existing roles for a user with a new set of roles.",
        request=ReplaceRolesSerializer,
        responses={200: UserRolesSerializer},
    )
    def put(self, request: Request, id: Any) -> Response:
        serializer = ReplaceRolesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(id=id).first()
        if not user:
            raise NotFound("User with specified ID does not exist.")

        roles_list = serializer.validated_data["roles"]
        RoleService.replace_roles(
            user=user, roles=roles_list, actor=request.user, request=request
        )

        user_roles = sorted(list(RoleService.get_roles(user)))
        return api_response(
            success=True,
            message="User roles replaced successfully.",
            data={"user_id": str(user.id), "roles": user_roles},
            status_code=status.HTTP_200_OK,
        )


class ClearRolesAPIView(APIView):
    """
    API endpoint clearing all roles from a user.
    """

    permission_classes = [IsAuthenticated, IsAdministratorRole]

    @extend_schema(
        tags=["RBAC Management"],
        summary="Clear user roles",
        description="Clears all roles assigned to a user.",
        responses={200: UserRolesSerializer},
    )
    def delete(self, request: Request, id: Any) -> Response:
        user = User.objects.filter(id=id).first()
        if not user:
            raise NotFound("User with specified ID does not exist.")

        RoleService.clear_roles(user=user, actor=request.user, request=request)

        return api_response(
            success=True,
            message="User roles cleared successfully.",
            data={"user_id": str(user.id), "roles": []},
            status_code=status.HTTP_200_OK,
        )

"""
Serializers for PawMatch RBAC (Role-Based Access Control) API endpoints.
"""

from rest_framework import serializers

from apps.accounts.roles import RoleName


class RoleDetailSerializer(serializers.Serializer):
    """Serializer representing platform role metadata and assigned permissions."""

    role = serializers.CharField(help_text="Platform role string constant.")
    display_name = serializers.CharField(
        help_text="Human-readable Django group display name."
    )
    permission_count = serializers.IntegerField(help_text="Total permissions count.")
    permissions = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of permission strings assigned to role.",
    )


class AssignRoleSerializer(serializers.Serializer):
    """Serializer for assigning a role to a user."""

    role = serializers.CharField(required=True, help_text="Role constant to assign.")

    def validate_role(self, value: str) -> str:
        normalized = value.strip().upper()
        if normalized not in RoleName.get_all_roles():
            raise serializers.ValidationError(
                f"Invalid role '{value}'. Must be a valid platform RoleName."
            )
        return normalized


class RemoveRoleSerializer(serializers.Serializer):
    """Serializer for removing a role from a user."""

    role = serializers.CharField(required=True, help_text="Role constant to remove.")

    def validate_role(self, value: str) -> str:
        normalized = value.strip().upper()
        if normalized not in RoleName.get_all_roles():
            raise serializers.ValidationError(
                f"Invalid role '{value}'. Must be a valid platform RoleName."
            )
        return normalized


class ReplaceRolesSerializer(serializers.Serializer):
    """Serializer for replacing all roles assigned to a user."""

    roles = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        allow_empty=True,
        help_text="New set of role constants to assign.",
    )

    def validate_roles(self, value: list) -> list:
        all_roles = RoleName.get_all_roles()
        normalized_list = []
        for role_str in value:
            normalized = role_str.strip().upper()
            if normalized not in all_roles:
                raise serializers.ValidationError(
                    f"Invalid role '{role_str}' in roles list."
                )
            normalized_list.append(normalized)
        return normalized_list


class UserRolesSerializer(serializers.Serializer):
    """Serializer representing user roles response payload."""

    user_id = serializers.UUIDField()
    roles = serializers.ListField(child=serializers.CharField())


class UserPermissionsSerializer(serializers.Serializer):
    """Serializer representing user permissions response payload."""

    user_id = serializers.UUIDField()
    permissions = serializers.ListField(child=serializers.CharField())

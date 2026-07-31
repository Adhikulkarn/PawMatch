"""
REST API serializers for PawMatch Authentication, User Registration & Email Verification.
"""

from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.validators import (
    validate_email_unique,
    validate_password_confirmation,
)


class LoginSerializer(serializers.Serializer):
    """Serializer for user authentication requests."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )


class LogoutSerializer(serializers.Serializer):
    """Serializer for refresh token blacklisting on logout."""

    refresh = serializers.CharField(required=True)


class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializer for returning current user profile details."""

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "profile_image",
            "is_email_verified",
        )
        read_only_fields = fields


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration requests."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        # Validate password confirmation & strength rules
        validate_password_confirmation(password, confirm_password)

        # Validate email uniqueness & normalization
        normalized_email = validate_email_unique(attrs.get("email", ""))

        attrs["email"] = normalized_email
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    """Serializer for email verification requests."""

    token = serializers.CharField(required=True)


class ResendVerificationSerializer(serializers.Serializer):
    """Serializer for resending email verification requests."""

    email = serializers.EmailField(required=True)

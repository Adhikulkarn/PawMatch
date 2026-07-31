"""
Profile service layer for PawMatch.
Encapsulates profile retrieval, personal info updates, avatar management, and account deactivation.
"""

import logging
from typing import Any, Dict, Optional, Tuple

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.accounts.constants import AuditAction, AuthMessage
from apps.accounts.events import EventDispatcher
from apps.accounts.exceptions import AuthenticationException
from apps.accounts.models import User, UserProfile
from apps.accounts.services.storage_service import StorageService
from apps.accounts.validators import validate_avatar_file, validate_phone_number
from apps.audit_logs.services.audit_service import AuditService

logger = logging.getLogger("apps.accounts")


class ProfileService:
    """
    Domain service executing user profile management business logic.
    """

    ALLOWED_USER_FIELDS = {"first_name", "last_name"}
    ALLOWED_PROFILE_FIELDS = {
        "phone_number",
        "bio",
        "date_of_birth",
        "preferences",
    }
    FORBIDDEN_FIELDS = {
        "email",
        "password",
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "permissions",
        "is_email_verified",
        "created_at",
        "updated_at",
        "last_login",
    }

    @classmethod
    def get_profile(cls, user: User) -> Tuple[User, UserProfile]:
        """
        Retrieves user and associated UserProfile instance, creating profile if missing.
        """
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return user, profile

    @classmethod
    @transaction.atomic
    def update_profile(
        cls, user: User, data: Dict[str, Any], request: Optional[Any] = None
    ) -> UserProfile:
        """
        Validates editable fields, updates User and UserProfile models,
        emits ProfileUpdatedEvent, and records security audit log.
        """
        # Reject forbidden or unknown fields
        for field in data.keys():
            if field in cls.FORBIDDEN_FIELDS:
                raise ValidationError(
                    {field: [f"Modifying field '{field}' is strictly prohibited."]}
                )
            if (
                field not in cls.ALLOWED_USER_FIELDS
                and field not in cls.ALLOWED_PROFILE_FIELDS
            ):
                raise ValidationError(
                    {field: [f"Unknown or uneditable field '{field}'."]}
                )

        profile, _ = UserProfile.objects.get_or_create(user=user)
        user_updated_fields = []
        profile_updated_fields = []

        # Update User model fields
        if "first_name" in data:
            user.first_name = data["first_name"]
            user_updated_fields.append("first_name")
        if "last_name" in data:
            user.last_name = data["last_name"]
            user_updated_fields.append("last_name")

        if user_updated_fields:
            user.save(update_fields=user_updated_fields)

        # Update UserProfile model fields
        if "phone_number" in data:
            validated_phone = validate_phone_number(data["phone_number"])
            profile.phone_number = validated_phone
            profile_updated_fields.append("phone_number")

        if "bio" in data:
            profile.bio = data["bio"]
            profile_updated_fields.append("bio")

        if "date_of_birth" in data:
            profile.date_of_birth = data["date_of_birth"]
            profile_updated_fields.append("date_of_birth")

        if "preferences" in data and isinstance(data["preferences"], dict):
            # Merge updated preference keys with existing preferences
            current_prefs = dict(profile.preferences)
            current_prefs.update(data["preferences"])
            profile.preferences = current_prefs
            profile_updated_fields.append("preferences")

        if profile_updated_fields:
            profile.save(update_fields=profile_updated_fields)

        all_updated = user_updated_fields + profile_updated_fields

        EventDispatcher.dispatch_profile_updated(
            user_id=user.id,
            email=user.email,
            updated_fields=all_updated,
            request=request,
        )

        AuditService.log_event(
            action=AuditAction.PROFILE_UPDATED,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
            details={"updated_fields": all_updated},
        )

        return profile

    @classmethod
    @transaction.atomic
    def upload_avatar(
        cls, user: User, avatar_file: Any, request: Optional[Any] = None
    ) -> str:
        """
        Validates avatar file, replaces existing avatar in media storage,
        updates UserProfile, emits AvatarUploadedEvent, and records audit trail.
        """
        validate_avatar_file(avatar_file)

        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Save avatar file via StorageService strategy
        saved_path = StorageService.save_avatar(avatar_file, user.id)
        profile.avatar = saved_path
        profile.save(update_fields=["avatar"])

        avatar_url = (
            profile.avatar.url
            if hasattr(profile.avatar, "url")
            else f"/media/{saved_path}"
        )

        EventDispatcher.dispatch_avatar_uploaded(
            user_id=user.id,
            email=user.email,
            avatar_url=avatar_url,
            request=request,
        )

        AuditService.log_event(
            action=AuditAction.AVATAR_UPLOADED,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
        )

        return avatar_url

    @classmethod
    @transaction.atomic
    def delete_avatar(cls, user: User, request: Optional[Any] = None) -> bool:
        """
        Deletes stored avatar file from media storage, resets UserProfile avatar to null,
        emits AvatarDeletedEvent, and records audit trail.
        """
        profile, _ = UserProfile.objects.get_or_create(user=user)

        if profile.avatar:
            StorageService.delete_avatar(profile.avatar.name)
            profile.avatar = None
            profile.save(update_fields=["avatar"])

        EventDispatcher.dispatch_avatar_deleted(
            user_id=user.id, email=user.email, request=request
        )

        AuditService.log_event(
            action=AuditAction.AVATAR_DELETED,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
        )

        return True

    @classmethod
    @transaction.atomic
    def deactivate_account(
        cls, user: User, password: str, request: Optional[Any] = None
    ) -> bool:
        """
        Validates user password, soft deactivates account (is_active=False),
        emits AccountDeactivatedEvent, and logs security audit.
        """
        if not password or not user.check_password(password):
            AuditService.log_event(
                action=AuditAction.ACCOUNT_DEACTIVATED,
                request=request,
                user_id=user.id,
                email=user.email,
                status="FAILED",
                details={"reason": AuthMessage.INCORRECT_PASSWORD},
            )
            raise AuthenticationException(AuthMessage.INCORRECT_PASSWORD)

        user.is_active = False
        user.save(update_fields=["is_active"])

        EventDispatcher.dispatch_account_deactivated(
            user_id=user.id, email=user.email, request=request
        )

        AuditService.log_event(
            action=AuditAction.ACCOUNT_DEACTIVATED,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
        )

        return True

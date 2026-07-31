"""
Password service layer for PawMatch.
Encapsulates secure password changes, forgot password workflows, token-based password resets,
and security notification emails.
"""

import logging
from datetime import timedelta
from typing import Any, Optional, Tuple

from django.db import transaction
from django.utils import timezone

from apps.accounts.config import accounts_config
from apps.accounts.constants import AuditAction, AuthMessage
from apps.accounts.events import EventDispatcher
from apps.accounts.exceptions import (
    InvalidCurrentPasswordException,
    InvalidTokenException,
)
from apps.accounts.models import AccountToken, AccountTokenType, User
from apps.accounts.services.email_service import EmailService
from apps.accounts.utils import generate_secure_raw_token, normalize_email_address
from apps.accounts.validators import (
    validate_password_confirmation,
    validate_password_not_reused,
    validate_password_not_same,
)
from apps.audit_logs.services.audit_service import AuditService

logger = logging.getLogger("apps.accounts")


class PasswordService:
    """
    Domain service executing password lifecycle management business logic.
    """

    @classmethod
    def generate_reset_token(cls, user: User) -> Tuple[AccountToken, str]:
        """
        Generates a cryptographically secure raw reset token, computes its SHA-256 hash,
        persists AccountToken (PASSWORD_RESET type), and returns (token_instance, raw_token).
        """
        raw_token = generate_secure_raw_token()
        token_hash = AccountToken.hash_token(raw_token)
        expires_at = timezone.now() + timedelta(
            hours=accounts_config.password_reset_expiry_hours
        )

        token_obj = AccountToken.objects.create(
            user=user,
            token_hash=token_hash,
            token_type=AccountTokenType.PASSWORD_RESET,
            expires_at=expires_at,
            is_active=True,
        )
        return token_obj, raw_token

    @classmethod
    @transaction.atomic
    def change_password(
        cls,
        user: User,
        current_password: str,
        new_password: str,
        confirm_password: str,
        request: Optional[Any] = None,
    ) -> bool:
        """
        Verifies current password, validates new password strength and uniqueness,
        updates hashed password, dispatches security email, and records audit trails.
        """
        if not current_password or not user.check_password(current_password):
            AuditService.log_event(
                action=AuditAction.PASSWORD_CHANGE_FAILED,
                request=request,
                user_id=user.id,
                email=user.email,
                status="FAILED",
                details={"reason": AuthMessage.INCORRECT_PASSWORD},
            )
            raise InvalidCurrentPasswordException(AuthMessage.INCORRECT_PASSWORD)

        validate_password_not_same(current_password, new_password)
        validate_password_confirmation(new_password, confirm_password)
        validate_password_not_reused(user, new_password)

        user.set_password(new_password)
        user.save(update_fields=["password"])

        EmailService.send_password_changed_email(user=user, request=request)

        EventDispatcher.dispatch_password_changed(
            user_id=user.id, email=user.email, request=request
        )

        AuditService.log_event(
            action=AuditAction.PASSWORD_CHANGED,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
        )

        return True

    @classmethod
    @transaction.atomic
    def forgot_password(cls, email: str, request: Optional[Any] = None) -> bool:
        """
        Initiates password reset process. Generates AccountToken and dispatches email if user exists.
        SECURITY: Always returns True regardless of email existence to prevent user enumeration.
        """
        normalized_email = normalize_email_address(email)
        user = User.objects.filter(email=normalized_email).first()

        if not user or not user.is_active:
            AuditService.log_event(
                action=AuditAction.PASSWORD_RESET_REQUESTED,
                request=request,
                email=normalized_email,
                status="FAILED",
                details={"reason": "User non-existent or inactive."},
            )
            return True

        # Invalidate previous active password reset tokens
        AccountToken.objects.filter(
            user=user,
            token_type=AccountTokenType.PASSWORD_RESET,
            is_active=True,
        ).update(is_active=False)

        token_obj, raw_token = cls.generate_reset_token(user)

        EmailService.send_password_reset_email(
            user=user, raw_token=raw_token, request=request
        )

        EventDispatcher.dispatch_password_reset_requested(
            user_id=user.id, email=user.email, request=request
        )

        AuditService.log_event(
            action=AuditAction.PASSWORD_RESET_REQUESTED,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
        )

        return True

    @classmethod
    @transaction.atomic
    def reset_password(
        cls,
        raw_token: str,
        new_password: str,
        confirm_password: str,
        request: Optional[Any] = None,
    ) -> bool:
        """
        Validates raw reset token, updates password, marks token as used,
        dispatches security confirmation email, and records audit trail.
        """
        if not raw_token:
            AuditService.log_event(
                action=AuditAction.PASSWORD_RESET_FAILED,
                request=request,
                status="FAILED",
                details={"reason": "Missing token parameter."},
            )
            raise InvalidTokenException("Password reset token is required.")

        token_hash = AccountToken.hash_token(raw_token)
        token_obj = AccountToken.objects.filter(
            token_hash=token_hash,
            token_type=AccountTokenType.PASSWORD_RESET,
        ).first()

        if not token_obj or not token_obj.is_valid():
            AuditService.log_event(
                action=AuditAction.PASSWORD_RESET_FAILED,
                request=request,
                status="FAILED",
                details={"reason": "Invalid, expired, or consumed reset token."},
            )
            raise InvalidTokenException(
                "Password reset token is invalid, expired, or already used."
            )

        user = token_obj.user
        validate_password_confirmation(new_password, confirm_password)
        validate_password_not_reused(user, new_password)

        user.set_password(new_password)
        user.save(update_fields=["password"])

        token_obj.mark_as_used()

        # Invalidate any other active reset tokens for this user
        AccountToken.objects.filter(
            user=user,
            token_type=AccountTokenType.PASSWORD_RESET,
            is_active=True,
        ).update(is_active=False)

        EmailService.send_password_changed_email(user=user, request=request)

        EventDispatcher.dispatch_password_reset_completed(
            user_id=user.id, email=user.email, request=request
        )

        AuditService.log_event(
            action=AuditAction.PASSWORD_RESET_COMPLETED,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
        )

        return True

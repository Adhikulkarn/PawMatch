"""
Domain registration service layer for PawMatch.
Encapsulates user registration, verification token generation, email verification,
and resending verification tokens with security audit trails.
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
    EmailAlreadyVerifiedException,
    InvalidTokenException,
    RegistrationException,
)
from apps.accounts.models import AccountToken, AccountTokenType, User
from apps.accounts.services.email_service import EmailService
from apps.accounts.utils import generate_secure_raw_token, normalize_email_address
from apps.accounts.validators import validate_email_unique
from apps.audit_logs.services.audit_service import AuditService

logger = logging.getLogger("apps.accounts")


class RegistrationService:
    """
    Domain service executing user onboarding business logic.
    """

    @classmethod
    def generate_verification_token(
        cls,
        user: User,
        token_type: str = AccountTokenType.EMAIL_VERIFICATION,
    ) -> Tuple[AccountToken, str]:
        """
        Generates a cryptographically secure URL-safe verification token, computes its SHA-256 hash,
        persists the AccountToken model, and returns (token_instance, raw_token).
        Raw tokens are NEVER stored in the database.
        """
        raw_token = generate_secure_raw_token()
        token_hash = AccountToken.hash_token(raw_token)
        expires_at = timezone.now() + timedelta(
            hours=accounts_config.email_verification_expiry_hours
        )

        token_obj = AccountToken.objects.create(
            user=user,
            token_hash=token_hash,
            token_type=token_type,
            expires_at=expires_at,
            is_active=True,
        )
        return token_obj, raw_token

    @classmethod
    @transaction.atomic
    def register_user(
        cls,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        request: Optional[Any] = None,
    ) -> Tuple[User, AccountToken, str]:
        """
        Registers a new inactive user, generates a secure verification token,
        dispatches a verification email, and logs a security audit record.
        """
        normalized_email = validate_email_unique(email)

        user = User.objects.create_user(
            email=normalized_email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_active=False,
            is_email_verified=False,
        )

        token_obj, raw_token = cls.generate_verification_token(user)

        EmailService.send_verification_email(
            user=user, raw_token=raw_token, request=request
        )

        EventDispatcher.dispatch_user_registered(
            user_id=user.id, email=user.email, request=request
        )

        AuditService.log_event(
            action=AuditAction.REGISTRATION_SUCCESS,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
        )

        return user, token_obj, raw_token

    @classmethod
    @transaction.atomic
    def verify_email_token(cls, raw_token: str, request: Optional[Any] = None) -> User:
        """
        Validates the raw verification token, activates the user account,
        marks the token as consumed, dispatches a welcome email, and records audit trails.
        """
        if not raw_token:
            AuditService.log_event(
                action=AuditAction.EMAIL_VERIFICATION_FAILED,
                request=request,
                status="FAILED",
                details={"reason": "Missing token parameter."},
            )
            raise InvalidTokenException("Verification token is required.")

        token_hash = AccountToken.hash_token(raw_token)
        token_obj = AccountToken.objects.filter(
            token_hash=token_hash,
            token_type=AccountTokenType.EMAIL_VERIFICATION,
        ).first()

        if not token_obj or not token_obj.is_valid():
            AuditService.log_event(
                action=AuditAction.EMAIL_VERIFICATION_FAILED,
                request=request,
                status="FAILED",
                details={"reason": "Invalid, expired, or consumed token."},
            )
            raise InvalidTokenException(
                "Verification token is invalid, expired, or already used."
            )

        user = token_obj.user
        user.is_active = True
        user.is_email_verified = True
        user.save(update_fields=["is_active", "is_email_verified"])

        token_obj.mark_as_used()

        # Invalidate any other active verification tokens for this user
        AccountToken.objects.filter(
            user=user,
            token_type=AccountTokenType.EMAIL_VERIFICATION,
            is_active=True,
        ).update(is_active=False)

        EmailService.send_welcome_email(user=user, request=request)

        EventDispatcher.dispatch_email_verified(
            user_id=user.id, email=user.email, request=request
        )

        AuditService.log_event(
            action=AuditAction.EMAIL_VERIFICATION_SUCCESS,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
        )

        return user

    @classmethod
    @transaction.atomic
    def resend_verification_email(
        cls, email: str, request: Optional[Any] = None
    ) -> bool:
        """
        Invalidates previous tokens, generates a fresh verification token,
        dispatches a verification email, and logs audit record.
        """
        normalized_email = normalize_email_address(email)
        user = User.objects.filter(email=normalized_email).first()

        if not user:
            AuditService.log_event(
                action=AuditAction.RESEND_VERIFICATION_FAILED,
                request=request,
                email=normalized_email,
                status="FAILED",
                details={"reason": AuthMessage.USER_NOT_FOUND},
            )
            raise RegistrationException({"email": [AuthMessage.USER_NOT_FOUND]})

        if user.is_email_verified:
            AuditService.log_event(
                action=AuditAction.RESEND_VERIFICATION_FAILED,
                request=request,
                user_id=user.id,
                email=user.email,
                status="FAILED",
                details={"reason": AuthMessage.EMAIL_ALREADY_VERIFIED},
            )
            raise EmailAlreadyVerifiedException(
                {"email": [AuthMessage.EMAIL_ALREADY_VERIFIED]}
            )

        # Invalidate previous unused active tokens
        AccountToken.objects.filter(
            user=user,
            token_type=AccountTokenType.EMAIL_VERIFICATION,
            is_active=True,
        ).update(is_active=False)

        token_obj, raw_token = cls.generate_verification_token(user)

        EmailService.send_verification_email(
            user=user, raw_token=raw_token, request=request
        )

        AuditService.log_event(
            action=AuditAction.VERIFICATION_EMAIL_RESENT,
            request=request,
            user_id=user.id,
            email=user.email,
            status="SUCCESS",
        )

        return True

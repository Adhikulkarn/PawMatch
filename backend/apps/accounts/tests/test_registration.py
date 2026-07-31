"""
Comprehensive unit and integration test suite for PawMatch User Registration,
AccountToken Lifecycle, Events, Validators, and Resend Verification APIs.
"""

from datetime import timedelta
from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from apps.accounts.config import accounts_config
from apps.accounts.events import user_registered_signal
from apps.accounts.models import AccountToken, AccountTokenType
from apps.accounts.services.registration_service import RegistrationService
from apps.accounts.validators import validate_phone_number
from apps.audit_logs.models import AuditLog

User = get_user_model()


class TestRegistrationAndVerification(APITestCase):
    """Test suite for User Registration, Email Verification, and AccountToken Lifecycle management."""

    def setUp(self):
        try:
            cache.clear()
        except Exception:
            pass

        self.register_url = reverse("accounts:register")
        self.verify_url = reverse("accounts:verify_email")
        self.resend_url = reverse("accounts:resend_verification")

        self.valid_payload = {
            "email": "newuser@example.com",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
            "first_name": "New",
            "last_name": "User",
        }

    def tearDown(self):
        try:
            cache.clear()
        except Exception:
            pass

    def test_successful_user_registration(self):
        """Tests registering a new user creates inactive account, token hash, email outbox message, and audit log."""
        response = self.client.post(
            self.register_url, self.valid_payload, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert "user" in response.data["data"]

        user = User.objects.get(email="newuser@example.com")
        assert user.is_active is False
        assert user.is_email_verified is False

        # Verify AccountToken created with token_hash and token_type EMAIL_VERIFICATION
        token_obj = AccountToken.objects.filter(
            user=user, token_type=AccountTokenType.EMAIL_VERIFICATION
        ).first()
        assert token_obj is not None
        assert token_obj.is_active is True
        assert token_obj.token_hash != ""

        # Verify email outbox contains 1 verification email
        assert len(mail.outbox) == 1
        assert "Verify your PawMatch Account" in mail.outbox[0].subject
        assert "newuser@example.com" in mail.outbox[0].to

        # Verify audit log recorded
        audit_entry = AuditLog.objects.filter(action="REGISTRATION_SUCCESS").first()
        assert audit_entry is not None
        assert audit_entry.email == "newuser@example.com"

    def test_register_duplicate_email(self):
        """Tests that registering with an existing email returns HTTP 400 validation error."""
        User.objects.create_user(
            email="newuser@example.com",
            first_name="Existing",
            last_name="User",
            password="Password123!",
        )

        response = self.client.post(
            self.register_url, self.valid_payload, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert "email" in response.data["errors"]

    def test_register_password_mismatch(self):
        """Tests registration fails when password and confirm_password do not match."""
        payload = self.valid_payload.copy()
        payload["confirm_password"] = "DifferentPassword123!"

        response = self.client.post(self.register_url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert "confirm_password" in response.data["errors"]

    def test_register_weak_password(self):
        """Tests registration fails when password does not meet Django security requirements."""
        payload = self.valid_payload.copy()
        payload["password"] = "123"
        payload["confirm_password"] = "123"

        response = self.client.post(self.register_url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False

    def test_email_verification_successful(self):
        """Tests verifying account with valid raw token activates user and dispatches welcome email."""
        user, _, raw_token = RegistrationService.register_user(
            email="verify@example.com",
            password="Password123!",
            first_name="Verify",
            last_name="User",
        )
        mail.outbox.clear()

        verify_res = self.client.get(f"{self.verify_url}?token={raw_token}")

        assert verify_res.status_code == status.HTTP_200_OK
        assert verify_res.data["success"] is True

        user.refresh_from_db()
        assert user.is_active is True
        assert user.is_email_verified is True

        # Verify welcome email sent
        assert len(mail.outbox) == 1
        assert "Welcome to PawMatch!" in mail.outbox[0].subject

        # Verify audit trail
        audit_entry = AuditLog.objects.filter(
            action="EMAIL_VERIFICATION_SUCCESS"
        ).first()
        assert audit_entry is not None

    def test_email_verification_invalid_token(self):
        """Tests verifying with invalid raw token returns HTTP 400 error."""
        verify_res = self.client.get(
            f"{self.verify_url}?token=invalid_raw_token_string"
        )

        assert verify_res.status_code == status.HTTP_400_BAD_REQUEST
        assert verify_res.data["success"] is False

    def test_email_verification_expired_token(self):
        """Tests verifying with an expired token returns HTTP 400 error."""
        user, token_obj, raw_token = RegistrationService.register_user(
            email="expired@example.com",
            password="Password123!",
            first_name="Expired",
            last_name="User",
        )

        # Manually expire token
        token_obj.expires_at = timezone.now() - timedelta(hours=1)
        token_obj.save()

        verify_res = self.client.get(f"{self.verify_url}?token={raw_token}")

        assert verify_res.status_code == status.HTTP_400_BAD_REQUEST
        assert verify_res.data["success"] is False

    def test_email_verification_reused_token(self):
        """Tests that a single-use token cannot be reused for a second verification attempt."""
        user, _, raw_token = RegistrationService.register_user(
            email="reused@example.com",
            password="Password123!",
            first_name="Reused",
            last_name="User",
        )

        # First verification succeeds
        first_res = self.client.get(f"{self.verify_url}?token={raw_token}")
        assert first_res.status_code == status.HTTP_200_OK

        # Second verification fails
        second_res = self.client.get(f"{self.verify_url}?token={raw_token}")
        assert second_res.status_code == status.HTTP_400_BAD_REQUEST

    def test_resend_verification_email_successful(self):
        """Tests resending verification email invalidates previous tokens and dispatches new email."""
        user, old_token_obj, _ = RegistrationService.register_user(
            email="resend@example.com",
            password="Password123!",
            first_name="Resend",
            last_name="User",
        )
        mail.outbox.clear()

        resend_res = self.client.post(
            self.resend_url, {"email": "resend@example.com"}, format="json"
        )

        assert resend_res.status_code == status.HTTP_200_OK
        assert resend_res.data["success"] is True

        old_token_obj.refresh_from_db()
        assert old_token_obj.is_active is False

        new_token_obj = AccountToken.objects.filter(
            user=user,
            token_type=AccountTokenType.EMAIL_VERIFICATION,
            is_active=True,
        ).first()
        assert new_token_obj is not None

        assert len(mail.outbox) == 1
        assert "Verify your PawMatch Account" in mail.outbox[0].subject

    def test_resend_verification_already_verified_user(self):
        """Tests resending verification for an already verified user returns HTTP 400."""
        User.objects.create_user(
            email="verified@example.com",
            first_name="Verified",
            last_name="User",
            password="Password123!",
            is_active=True,
            is_email_verified=True,
        )

        resend_res = self.client.post(
            self.resend_url, {"email": "verified@example.com"}, format="json"
        )

        assert resend_res.status_code == status.HTTP_400_BAD_REQUEST
        assert resend_res.data["success"] is False

    def test_resend_verification_unknown_email(self):
        """Tests resending verification for non-existent email returns HTTP 400."""
        resend_res = self.client.post(
            self.resend_url, {"email": "nonexistent@example.com"}, format="json"
        )

        assert resend_res.status_code == status.HTTP_400_BAD_REQUEST
        assert resend_res.data["success"] is False

    def test_account_token_generic_types_and_metadata(self):
        """Tests generic AccountToken supports multiple token types and JSON metadata."""
        user = User.objects.create_user(
            email="token_test@example.com",
            first_name="Token",
            last_name="Test",
            password="Password123!",
        )

        token = AccountToken.objects.create(
            user=user,
            token_hash="hash123",
            token_type=AccountTokenType.PASSWORD_RESET,
            expires_at=timezone.now() + timedelta(hours=1),
            metadata={"device": "mobile_app"},
        )

        assert token.token_type == AccountTokenType.PASSWORD_RESET
        assert token.metadata["device"] == "mobile_app"
        assert str(token).startswith("[PASSWORD_RESET]")

    def test_phone_number_validator(self):
        """Tests phone number validator accepts valid formats and rejects invalid formats."""
        assert validate_phone_number("+1234567890") == "+1234567890"
        assert validate_phone_number("123-456-7890") == "1234567890"
        assert validate_phone_number("") == ""

        try:
            validate_phone_number("invalid_phone")
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

    def test_event_dispatcher_signal(self):
        """Tests event signal dispatching for user registration."""
        mock_handler = MagicMock()
        user_registered_signal.connect(mock_handler)

        self.client.post(self.register_url, self.valid_payload, format="json")

        assert mock_handler.called is True
        user_registered_signal.disconnect(mock_handler)

    def test_accounts_config_defaults(self):
        """Tests accounts_config property accessors."""
        assert accounts_config.email_verification_expiry_hours == 24
        assert "http" in accounts_config.frontend_url
        assert accounts_config.email_provider_backend == "SMTP"

"""
Comprehensive unit and integration test suite for PawMatch User Profile Management,
Avatar Media Storage, Preference Management, and Account Deactivation APIs.
"""

from io import BytesIO
from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.events import (
    account_deactivated_signal,
    avatar_deleted_signal,
    avatar_uploaded_signal,
    profile_updated_signal,
)
from apps.accounts.models import UserProfile
from apps.audit_logs.models import AuditLog

User = get_user_model()


def generate_test_image(
    filename="test.png", ext="PNG", size=(100, 100), color=(255, 0, 0)
):
    """Helper to generate a valid in-memory test image file."""
    file = BytesIO()
    image = Image.new("RGB", size, color)
    image.save(file, ext)
    file.seek(0)
    content_type = f"image/{ext.lower()}"
    return SimpleUploadedFile(filename, file.read(), content_type=content_type)


class TestUserProfileManagement(APITestCase):
    """Test suite for User Profile APIs, Avatar upload/delete, Preferences, and Account Deactivation."""

    def setUp(self):
        try:
            cache.clear()
        except Exception:
            pass

        self.password = "StrongPassword123!"
        self.user = User.objects.create_user(
            email="profileuser@example.com",
            password=self.password,
            first_name="Profile",
            last_name="Tester",
            is_active=True,
            is_email_verified=True,
        )
        self.client.force_authenticate(user=self.user)

        self.profile_url = reverse("accounts:profile")
        self.avatar_url = reverse("accounts:avatar")
        self.deactivate_url = reverse("accounts:deactivate")

    def tearDown(self):
        try:
            cache.clear()
        except Exception:
            pass

    def test_get_profile_success(self):
        """Tests GET /api/v1/accounts/profile/ returns comprehensive user profile data."""
        response = self.client.get(self.profile_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        data = response.data["data"]

        assert data["email"] == "profileuser@example.com"
        assert data["first_name"] == "Profile"
        assert data["last_name"] == "Tester"
        assert "preferences" in data
        assert "is_email_verified" in data
        assert data["is_email_verified"] is True

    def test_update_profile_success(self):
        """Tests PATCH /api/v1/accounts/profile/ updates personal info and preferences, emitting signal and audit log."""
        mock_handler = MagicMock()
        profile_updated_signal.connect(mock_handler)

        payload = {
            "first_name": "UpdatedFirst",
            "last_name": "UpdatedLast",
            "phone_number": "+1234567890",
            "bio": "Pet lover and adopter.",
            "date_of_birth": "1995-05-15",
            "preferences": {"email_notifications": False, "theme": "dark"},
        }

        response = self.client.patch(self.profile_url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

        self.user.refresh_from_db()
        assert self.user.first_name == "UpdatedFirst"
        assert self.user.last_name == "UpdatedLast"

        profile = UserProfile.objects.get(user=self.user)
        assert profile.phone_number == "+1234567890"
        assert profile.bio == "Pet lover and adopter."
        assert str(profile.date_of_birth) == "1995-05-15"
        assert profile.preferences["email_notifications"] is False
        assert profile.preferences["theme"] == "dark"

        assert mock_handler.called is True
        profile_updated_signal.disconnect(mock_handler)

        # Audit log check
        audit_entry = AuditLog.objects.filter(action="PROFILE_UPDATED").first()
        assert audit_entry is not None

    def test_update_profile_forbidden_fields_rejected(self):
        """Tests updating forbidden fields (email, is_staff, is_active) returns HTTP 400 error."""
        response = self.client.patch(
            self.profile_url, {"email": "hacked@example.com"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False

        response_staff = self.client.patch(
            self.profile_url, {"is_staff": True}, format="json"
        )
        assert response_staff.status_code == status.HTTP_400_BAD_REQUEST

    def test_upload_avatar_success(self):
        """Tests uploading a valid image avatar updates profile, dispatches event signal and audit log."""
        mock_handler = MagicMock()
        avatar_uploaded_signal.connect(mock_handler)

        test_img = generate_test_image()
        response = self.client.post(
            self.avatar_url, {"avatar": test_img}, format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert "avatar" in response.data["data"]

        profile = UserProfile.objects.get(user=self.user)
        assert profile.avatar is not None
        assert profile.avatar.name != ""

        assert mock_handler.called is True
        avatar_uploaded_signal.disconnect(mock_handler)

        audit_entry = AuditLog.objects.filter(action="AVATAR_UPLOADED").first()
        assert audit_entry is not None

    def test_upload_avatar_invalid_extension_rejected(self):
        """Tests uploading a file with disallowed extension (.gif/.svg/.exe) returns HTTP 400 error."""
        invalid_file = SimpleUploadedFile(
            "script.exe", b"binary content", content_type="application/octet-stream"
        )

        response = self.client.post(
            self.avatar_url, {"avatar": invalid_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert "avatar" in response.data["errors"]

    def test_upload_avatar_oversized_rejected(self):
        """Tests uploading an oversized avatar file (>5MB) returns HTTP 400 error."""
        oversized_content = b"x" * (6 * 1024 * 1024)
        oversized_file = SimpleUploadedFile(
            "huge.jpg", oversized_content, content_type="image/jpeg"
        )

        response = self.client.post(
            self.avatar_url, {"avatar": oversized_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False

    def test_delete_avatar_success(self):
        """Tests deleting profile avatar removes stored image and resets field to null."""
        mock_handler = MagicMock()
        avatar_deleted_signal.connect(mock_handler)

        # Upload first
        test_img = generate_test_image()
        self.client.post(self.avatar_url, {"avatar": test_img}, format="multipart")

        # Delete
        response = self.client.delete(self.avatar_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

        profile = UserProfile.objects.get(user=self.user)
        assert bool(profile.avatar) is False

        assert mock_handler.called is True
        avatar_deleted_signal.disconnect(mock_handler)

        audit_entry = AuditLog.objects.filter(action="AVATAR_DELETED").first()
        assert audit_entry is not None

    def test_account_deactivation_successful(self):
        """Tests account deactivation with correct password soft-deactivates user (is_active=False)."""
        mock_handler = MagicMock()
        account_deactivated_signal.connect(mock_handler)

        response = self.client.post(
            self.deactivate_url, {"password": self.password}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

        self.user.refresh_from_db()
        assert self.user.is_active is False

        assert mock_handler.called is True
        account_deactivated_signal.disconnect(mock_handler)

        audit_entry = AuditLog.objects.filter(action="ACCOUNT_DEACTIVATED").first()
        assert audit_entry is not None
        assert audit_entry.status == "SUCCESS"

    def test_account_deactivation_incorrect_password(self):
        """Tests account deactivation with wrong password returns HTTP 401 error."""
        response = self.client.post(
            self.deactivate_url, {"password": "WrongPassword123!"}, format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["success"] is False

        self.user.refresh_from_db()
        assert self.user.is_active is True

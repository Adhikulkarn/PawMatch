"""
Comprehensive unit and integration test suite for PawMatch JWT Authentication APIs,
Rate Limiting Throttles, Security Audit Trails, and Standardized Responses.
"""

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.audit_logs.models import AuditLog

User = get_user_model()


class TestJWTAuthentication(APITestCase):
    """Test suite for JWT Authentication login, logout, refresh, current user endpoints, and security hardening."""

    def setUp(self):
        try:
            cache.clear()
        except Exception:
            pass

        self.login_url = reverse("accounts:login")
        self.logout_url = reverse("accounts:logout")
        self.refresh_url = reverse("accounts:token_refresh")
        self.me_url = reverse("accounts:me")

        self.password = "StrongPassword123!"
        self.active_user = User.objects.create_user(
            email="user@pawmatch.com",
            first_name="Active",
            last_name="User",
            password=self.password,
        )

        self.inactive_user = User.objects.create_user(
            email="inactive@pawmatch.com",
            first_name="Inactive",
            last_name="User",
            password=self.password,
            is_active=False,
        )

    def tearDown(self):
        try:
            cache.clear()
        except Exception:
            pass

    def test_successful_login_response_structure(self):
        """Tests authenticating with valid credentials returns standardized API response."""
        response = self.client.post(
            self.login_url,
            {"email": "user@pawmatch.com", "password": self.password},
            format="json",
            HTTP_USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Login successful."
        assert "data" in response.data

        data = response.data["data"]
        assert "access" in data
        assert "refresh" in data
        assert "user" in data
        assert data["user"]["email"] == "user@pawmatch.com"
        assert data["user"]["full_name"] == "Active User"

    def test_audit_log_creation_on_login(self):
        """Tests that successful login records an AuditLog entry with client metadata."""
        self.client.post(
            self.login_url,
            {"email": "user@pawmatch.com", "password": self.password},
            format="json",
            HTTP_USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Firefox/115.0",
        )

        audit_entry = AuditLog.objects.filter(action="LOGIN_SUCCESS").first()
        assert audit_entry is not None
        assert audit_entry.user_id == self.active_user.id
        assert audit_entry.email == "user@pawmatch.com"
        assert audit_entry.status == "SUCCESS"
        assert audit_entry.browser == "Firefox"
        assert audit_entry.os == "macOS"
        assert audit_entry.device_type == "Desktop"
        assert audit_entry.request_id != ""

    def test_login_invalid_password_audit(self):
        """Tests login attempt with invalid password creates failed audit log."""
        response = self.client.post(
            self.login_url,
            {"email": "user@pawmatch.com", "password": "WrongPassword!"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["success"] is False
        assert response.data["message"] == "Invalid email or password."

        audit_entry = AuditLog.objects.filter(action="LOGIN_FAILED_CREDENTIALS").first()
        assert audit_entry is not None
        assert audit_entry.email == "user@pawmatch.com"
        assert audit_entry.status == "FAILED"

    def test_login_disabled_account_audit(self):
        """Tests login attempt for inactive user account creates audit trail and returns 401."""
        response = self.client.post(
            self.login_url,
            {"email": "inactive@pawmatch.com", "password": self.password},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["success"] is False
        assert response.data["message"] == "Your account has been disabled."

        audit_entry = AuditLog.objects.filter(action="LOGIN_FAILED_DISABLED").first()
        assert audit_entry is not None
        assert audit_entry.email == "inactive@pawmatch.com"
        assert audit_entry.status == "FAILED"

    def test_login_rate_limiting(self):
        """Tests DRF rate limiting throttle on login endpoint (5 attempts/min limit)."""
        # Execute 5 allowed login attempts
        for _ in range(5):
            self.client.post(
                self.login_url,
                {"email": "user@pawmatch.com", "password": "WrongPassword!"},
                format="json",
            )

        # 6th attempt should trigger HTTP 429 Too Many Requests
        response = self.client.post(
            self.login_url,
            {"email": "user@pawmatch.com", "password": "WrongPassword!"},
            format="json",
        )

        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert response.data["success"] is False
        assert "Request was throttled" in response.data["message"]

    def test_token_refresh_successful(self):
        """Tests obtaining a new access token using a valid refresh token."""
        login_res = self.client.post(
            self.login_url,
            {"email": "user@pawmatch.com", "password": self.password},
            format="json",
        )
        refresh_token = login_res.data["data"]["refresh"]

        refresh_res = self.client.post(
            self.refresh_url,
            {"refresh": refresh_token},
            format="json",
        )

        assert refresh_res.status_code == status.HTTP_200_OK
        assert refresh_res.data["success"] is True
        assert "access" in refresh_res.data["data"]

        audit_entry = AuditLog.objects.filter(action="TOKEN_REFRESH_SUCCESS").first()
        assert audit_entry is not None

    def test_successful_logout(self):
        """Tests logging out by blacklisting the active refresh token."""
        login_res = self.client.post(
            self.login_url,
            {"email": "user@pawmatch.com", "password": self.password},
            format="json",
        )
        access_token = login_res.data["data"]["access"]
        refresh_token = login_res.data["data"]["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        logout_res = self.client.post(
            self.logout_url,
            {"refresh": refresh_token},
            format="json",
        )

        assert logout_res.status_code == status.HTTP_200_OK
        assert logout_res.data["success"] is True
        assert logout_res.data["message"] == "Successfully logged out."

        audit_entry = AuditLog.objects.filter(action="LOGOUT_SUCCESS").first()
        assert audit_entry is not None

    def test_blacklisted_token_cannot_be_refreshed(self):
        """Tests that a blacklisted refresh token cannot be reused."""
        login_res = self.client.post(
            self.login_url,
            {"email": "user@pawmatch.com", "password": self.password},
            format="json",
        )
        access_token = login_res.data["data"]["access"]
        refresh_token = login_res.data["data"]["refresh"]

        # Logout to blacklist token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.client.post(
            self.logout_url,
            {"refresh": refresh_token},
            format="json",
        )

        # Attempt refresh with blacklisted token
        refresh_res = self.client.post(
            self.refresh_url,
            {"refresh": refresh_token},
            format="json",
        )

        assert refresh_res.status_code == status.HTTP_401_UNAUTHORIZED
        assert refresh_res.data["success"] is False

    def test_authenticated_me_endpoint(self):
        """Tests retrieving current user profile with valid Bearer token."""
        login_res = self.client.post(
            self.login_url,
            {"email": "user@pawmatch.com", "password": self.password},
            format="json",
        )
        access_token = login_res.data["data"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        me_res = self.client.get(self.me_url)

        assert me_res.status_code == status.HTTP_200_OK
        assert me_res.data["success"] is True
        assert me_res.data["data"]["email"] == "user@pawmatch.com"
        assert me_res.data["data"]["full_name"] == "Active User"

    def test_unauthenticated_me_endpoint(self):
        """Tests accessing /me endpoint without authentication credentials returns HTTP 401."""
        me_res = self.client.get(self.me_url)

        assert me_res.status_code == status.HTTP_401_UNAUTHORIZED
        assert me_res.data["success"] is False

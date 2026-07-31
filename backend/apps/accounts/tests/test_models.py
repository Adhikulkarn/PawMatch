"""
Unit tests for the Custom User model and CustomUserManager in PawMatch.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestCustomUserModel(TestCase):
    """Test suite for Custom User model and manager operations."""

    def test_create_user_successful(self):
        """Tests creating a standard user with valid details."""
        user = User.objects.create_user(
            email="TEST.USER@example.com",
            first_name="Jane",
            last_name="Doe",
            password="SecurePassword123!",
        )

        assert user.email == "test.user@example.com"
        assert user.first_name == "Jane"
        assert user.last_name == "Doe"
        assert user.full_name == "Jane Doe"
        assert user.get_full_name() == "Jane Doe"
        assert user.get_short_name() == "Jane"
        assert str(user) == "test.user@example.com"
        assert user.check_password("SecurePassword123!") is True
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.is_email_verified is False
        assert user.id is not None

    def test_create_user_missing_required_fields(self):
        """Tests that creating a user without email, first name, or last name raises ValueError."""
        with pytest.raises(ValueError, match="The Email field must be set"):
            User.objects.create_user(
                email="",
                first_name="Jane",
                last_name="Doe",
                password="password123",
            )

        with pytest.raises(ValueError, match="The First Name field must be set"):
            User.objects.create_user(
                email="jane@example.com",
                first_name="",
                last_name="Doe",
                password="password123",
            )

        with pytest.raises(ValueError, match="The Last Name field must be set"):
            User.objects.create_user(
                email="jane@example.com",
                first_name="Jane",
                last_name="",
                password="password123",
            )

    def test_create_superuser_successful(self):
        """Tests creating a superuser with admin privileges."""
        admin_user = User.objects.create_superuser(
            email="admin@pawmatch.com",
            first_name="Admin",
            last_name="User",
            password="AdminPassword123!",
        )

        assert admin_user.email == "admin@pawmatch.com"
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True
        assert admin_user.is_active is True
        assert admin_user.is_email_verified is True

    def test_create_superuser_invalid_flags(self):
        """Tests that creating a superuser with invalid flag overrides raises ValueError."""
        with pytest.raises(ValueError, match="Superuser must have is_staff=True"):
            User.objects.create_superuser(
                email="admin2@pawmatch.com",
                first_name="Admin",
                last_name="User",
                password="AdminPassword123!",
                is_staff=False,
            )

        with pytest.raises(ValueError, match="Superuser must have is_superuser=True"):
            User.objects.create_superuser(
                email="admin3@pawmatch.com",
                first_name="Admin",
                last_name="User",
                password="AdminPassword123!",
                is_superuser=False,
            )

    def test_user_soft_delete_and_restore(self):
        """Tests soft delete and restoration capabilities on User model."""
        user = User.objects.create_user(
            email="softdelete@example.com",
            first_name="Soft",
            last_name="Delete",
            password="password123",
        )

        assert user.is_deleted is False
        assert user.deleted_at is None

        user.soft_delete()
        user.refresh_from_db()

        assert user.is_deleted is True
        assert user.deleted_at is not None

        user.restore()
        user.refresh_from_db()

        assert user.is_deleted is False
        assert user.deleted_at is None

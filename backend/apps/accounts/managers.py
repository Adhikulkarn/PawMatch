"""
Custom model manager for the PawMatch User model.
"""

from typing import Any, Optional

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def normalize_email(self, email: str) -> str:
        """
        Normalizes the email address by stripping whitespace and lowercasing
        both the local and domain parts via Django's BaseUserManager.normalize_email.
        This guarantees complete case-insensitive email uniqueness across the system.
        """
        normalized_email = super().normalize_email(email)
        return normalized_email.strip().lower()

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> Any:
        """
        Creates and saves a User with the given email, first_name, last_name, and password.
        """
        if not email:
            raise ValueError(_("The Email field must be set."))
        if not first_name:
            raise ValueError(_("The First Name field must be set."))
        if not last_name:
            raise ValueError(_("The Last Name field must be set."))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> Any:
        """
        Creates and saves a Superuser with the given email, first_name, last_name, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_email_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser must have is_active=True."))

        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields,
        )

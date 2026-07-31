"""
Custom User model definition for PawMatch.

Architecture Note — Profile Separation:
This User model serves strictly as the authentication and core identity entity.
Domain-specific profiles will be attached via OneToOne relationships in future phases:
    User
    ├── AdopterProfile
    ├── ShelterProfile
    ├── VolunteerProfile
    ├── VeterinarianProfile
    ├── ModeratorProfile
    └── AdministratorProfile
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import CustomUserManager
from apps.core.mixins import SoftDeleteModel, TimestampedModel, UUIDModel


class User(
    AbstractBaseUser,
    PermissionsMixin,
    UUIDModel,
    TimestampedModel,
    SoftDeleteModel,
):
    """
    Production-ready custom User model for PawMatch.
    Uses email for primary authentication instead of usernames.
    Contains strictly identity, contact, basic profile, and authentication flags.
    """

    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    phone_number = models.CharField(
        _("phone number"),
        max_length=30,
        blank=True,
        default="",
    )
    profile_image = models.ImageField(
        _("profile image"),
        upload_to="users/profile_images/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user account should be treated as active."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_email_verified = models.BooleanField(
        _("email verified"),
        default=False,
        help_text=_("Designates whether this user has verified their email address."),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_full_name(self) -> str:
        """Django compatibility helper returning full name."""
        return self.full_name

    def get_short_name(self) -> str:
        """Django compatibility helper returning first name."""
        return self.first_name

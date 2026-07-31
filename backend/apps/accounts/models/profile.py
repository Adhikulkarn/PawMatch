"""
UserProfile model definition for PawMatch.
Maintains identity and personal profile details separate from core authentication model.
"""

from typing import Any, Dict

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.constants import DEFAULT_USER_PREFERENCES
from apps.core.mixins import TimestampedModel, UUIDModel


def default_profile_preferences() -> Dict[str, Any]:
    """Returns copy of default preference dictionary for JSONField."""
    return dict(DEFAULT_USER_PREFERENCES)


class UserProfile(UUIDModel, TimestampedModel):
    """
    Dedicated user profile model connected via OneToOne relationship to User.
    Stores non-authentication profile details, avatar, bio, and preferences.
    """

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="profile",
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=30,
        blank=True,
        default="",
    )
    avatar = models.ImageField(
        _("avatar image"),
        upload_to="users/avatars/",
        blank=True,
        null=True,
    )
    bio = models.TextField(
        _("bio"),
        blank=True,
        default="",
    )
    date_of_birth = models.DateField(
        _("date of birth"),
        null=True,
        blank=True,
    )
    preferences = models.JSONField(
        _("user preferences"),
        default=default_profile_preferences,
        blank=True,
    )

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Profile of {self.user.email}"

"""
Generic AccountToken model definition for PawMatch.
Provides reusable token infrastructure for Email Verification, Password Reset, Email Change, etc.
"""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.utils import hash_token
from apps.core.mixins import TimestampedModel, UUIDModel


class AccountTokenType(models.TextChoices):
    """Supported account token category types."""

    EMAIL_VERIFICATION = "EMAIL_VERIFICATION", _("Email Verification")
    PASSWORD_RESET = "PASSWORD_RESET", _("Password Reset")
    EMAIL_CHANGE = "EMAIL_CHANGE", _("Email Change")
    ACCOUNT_INVITATION = "ACCOUNT_INVITATION", _("Account Invitation")


class AccountToken(UUIDModel, TimestampedModel):
    """
    Generic cryptographically secure single-use account token model.
    Stores SHA-256 hashes of raw tokens for security against database leaks.
    """

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="account_tokens",
    )
    token_hash = models.CharField(
        _("token hash"),
        max_length=128,
        db_index=True,
    )
    token_type = models.CharField(
        _("token type"),
        max_length=32,
        choices=AccountTokenType.choices,
        default=AccountTokenType.EMAIL_VERIFICATION,
        db_index=True,
    )
    expires_at = models.DateTimeField(
        _("expires at"),
        db_index=True,
    )
    used_at = models.DateTimeField(
        _("used at"),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        db_index=True,
    )
    metadata = models.JSONField(
        _("metadata"),
        default=dict,
        blank=True,
    )

    class Meta:
        verbose_name = _("account token")
        verbose_name_plural = _("account tokens")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["token_hash"]),
            models.Index(fields=["token_type", "is_active"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self) -> str:
        return f"[{self.token_type}] Token for {self.user.email} (Active: {self.is_active})"

    @classmethod
    def hash_token(cls, raw_token: str) -> str:
        """Computes a SHA-256 hash of the raw token string for secure storage."""
        return hash_token(raw_token)

    def is_valid(self) -> bool:
        """Returns True if the token is active, unused, and unexpired."""
        return (
            self.is_active and self.used_at is None and timezone.now() < self.expires_at
        )

    def mark_as_used(self) -> None:
        """Marks token as consumed."""
        self.used_at = timezone.now()
        self.is_active = False
        self.save(update_fields=["used_at", "is_active"])

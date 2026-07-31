"""
Centralized configuration module for PawMatch Accounts.
Reads from Django settings while providing safe defaults.
"""

from django.conf import settings


class AccountsConfig:
    """Centralized accounts settings accessor."""

    @property
    def email_verification_expiry_hours(self) -> int:
        return getattr(settings, "EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS", 24)

    @property
    def frontend_url(self) -> str:
        return getattr(settings, "FRONTEND_URL", "http://localhost:5173")

    @property
    def frontend_verify_email_url(self) -> str:
        return getattr(
            settings,
            "FRONTEND_VERIFY_EMAIL_URL",
            f"{self.frontend_url}/verify-email",
        )

    @property
    def default_token_bytes(self) -> int:
        return getattr(settings, "ACCOUNTS_DEFAULT_TOKEN_BYTES", 32)

    @property
    def email_provider_backend(self) -> str:
        return getattr(settings, "ACCOUNTS_EMAIL_PROVIDER", "SMTP").upper()


accounts_config = AccountsConfig()

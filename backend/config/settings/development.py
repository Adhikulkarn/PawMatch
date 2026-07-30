"""
Development settings for PawMatch.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["127.0.0.1", "localhost", "*"],
)

# Email output directed to terminal console in development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database Configuration Fallback
if not env.str("DATABASE_URL", default=""):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Development CORS Settings
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=True)

# Verbose Development Logging
LOG_LEVEL = "DEBUG"
LOGGING = get_logging_config(BASE_DIR, LOG_LEVEL)

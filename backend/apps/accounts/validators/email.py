"""
Email validation functions for PawMatch Accounts.
"""

from typing import Any, Optional

from rest_framework.exceptions import ValidationError

from apps.accounts.utils import normalize_email_address


def validate_email_unique(email: str, model_class: Any = None) -> str:
    """
    Normalizes email and validates that no user exists with the same email.
    """
    from apps.accounts.models import User

    normalized_email = normalize_email_address(email)

    target_model = model_class or User
    if target_model.objects.filter(email=normalized_email).exists():
        raise ValidationError({"email": ["A user with that email already exists."]})

    return normalized_email

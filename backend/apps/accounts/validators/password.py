"""
Password validation functions for PawMatch Accounts.
"""

from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


def validate_password_confirmation(password: str, confirm_password: str) -> None:
    """
    Validates that password and confirm_password match and runs Django password strength rules.
    """
    if password != confirm_password:
        raise ValidationError({"confirm_password": ["Passwords do not match."]})

    validate_password(password)

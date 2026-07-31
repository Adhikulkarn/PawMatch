"""
Password validation functions for PawMatch Accounts.
"""

from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

from apps.accounts.constants import AuthMessage


def validate_password_confirmation(password: str, confirm_password: str) -> None:
    """
    Validates that password and confirm_password match and runs Django password strength rules.
    """
    if password != confirm_password:
        raise ValidationError({"confirm_password": [AuthMessage.PASSWORD_MISMATCH]})

    validate_password(password)


def validate_password_not_same(current_password: str, new_password: str) -> None:
    """
    Validates that new password is not identical to current password.
    """
    if current_password == new_password:
        raise ValidationError({"new_password": [AuthMessage.SAME_PASSWORD_ERROR]})


def validate_password_not_reused(user: Any, new_password: str) -> None:
    """
    Validates that new password is not identical to user's existing password.
    """
    if user and user.check_password(new_password):
        raise ValidationError({"new_password": [AuthMessage.PASSWORD_REUSE_ERROR]})

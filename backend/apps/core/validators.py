"""
Core infrastructure field validators for PawMatch.
"""

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# E.164 Phone Number Regex
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def validate_phone_number(value: str) -> None:
    """Validates that a string adheres to E.164 international phone formatting."""
    if value and not PHONE_REGEX.match(value):
        raise ValidationError(
            _(
                "Phone number must be entered in E.164 format: '+1234567890' (up to 15 digits)."
            ),
            code="invalid_phone_number",
        )


def validate_file_size(file_obj, max_size_mb: int = 5) -> None:
    """Validates uploaded file size does not exceed specified limit in MB."""
    max_bytes = max_size_mb * 1024 * 1024
    if file_obj and file_obj.size > max_bytes:
        raise ValidationError(
            _("File size must not exceed %(max_size)s MB."),
            params={"max_size": max_size_mb},
            code="file_size_exceeded",
        )

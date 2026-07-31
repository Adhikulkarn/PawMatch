"""
Phone number validation functions for PawMatch Accounts.
"""

import re

from rest_framework.exceptions import ValidationError


def validate_phone_number(phone_number: str) -> str:
    """
    Validates optional phone number format.
    """
    if not phone_number:
        return ""
    cleaned = re.sub(r"[\s\-\(\)]", "", phone_number)
    if not re.match(r"^\+?[0-9]{7,15}$", cleaned):
        raise ValidationError({"phone_number": ["Enter a valid phone number."]})
    return cleaned

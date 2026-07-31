"""
Image validation functions for PawMatch avatar uploads.
"""

import os
from typing import Any

from rest_framework.exceptions import ValidationError

from apps.accounts.config import accounts_config


def validate_avatar_file(file_obj: Any) -> Any:
    """
    Validates uploaded avatar image file for size, file extension, and MIME content-type.
    """
    if not file_obj:
        raise ValidationError({"avatar": ["No file was provided."]})

    # 1. Size Validation
    max_bytes = accounts_config.max_avatar_size_bytes
    if file_obj.size > max_bytes:
        max_mb = max_bytes / (1024 * 1024)
        raise ValidationError(
            {"avatar": [f"File size exceeds maximum allowed limit of {max_mb:.0f}MB."]}
        )

    # 2. Extension Validation
    ext = os.path.splitext(file_obj.name)[1].lower()
    allowed_extensions = accounts_config.allowed_avatar_extensions
    if ext not in allowed_extensions:
        raise ValidationError(
            {
                "avatar": [
                    f"Invalid file extension '{ext}'. Allowed extensions are: {', '.join(allowed_extensions)}."
                ]
            }
        )

    # 3. Content Type Validation
    content_type = getattr(file_obj, "content_type", "").lower()
    allowed_types = accounts_config.allowed_avatar_types
    if content_type and content_type not in allowed_types:
        raise ValidationError(
            {
                "avatar": [
                    f"Unsupported image type '{content_type}'. Allowed types are JPG, PNG, and WEBP."
                ]
            }
        )

    return file_obj

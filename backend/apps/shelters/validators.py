"""
Custom validators for Shelter domain models and document uploads.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MAX_DOCUMENT_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit
ALLOWED_DOCUMENT_MIME_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png",
]


def validate_document_file_size(file):
    """Validates that uploaded document size does not exceed MAX_DOCUMENT_FILE_SIZE_BYTES."""
    if file.size > MAX_DOCUMENT_FILE_SIZE_BYTES:
        raise ValidationError(
            _("File size exceeds maximum allowed threshold of 10 MB.")
        )


def validate_document_mime_type(file):
    """Validates that uploaded document mime type / extension is supported."""
    content_type = getattr(file, "content_type", None)
    if content_type and content_type.lower() not in ALLOWED_DOCUMENT_MIME_TYPES:
        raise ValidationError(
            _("Unsupported file type '%(type)s'. Allowed types: PDF, JPEG, PNG.")
            % {"type": content_type}
        )

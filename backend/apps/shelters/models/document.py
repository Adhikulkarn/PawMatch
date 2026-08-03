"""
ShelterDocument entity definition representing uploaded legal & verification documents.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.mixins import TimestampedModel, UUIDModel
from apps.shelters.constants import DocumentStatus, DocumentType
from apps.shelters.validators import (
    validate_document_file_size,
    validate_document_mime_type,
)


class ShelterDocument(UUIDModel, TimestampedModel):
    """
    Represents legal and identification documents uploaded by shelters for verification.

    Document Types:
    - Registration Certificate
    - NGO Certificate
    - Government License
    - Address Proof
    - Identity Proof
    - Tax Certificate
    - Other

    Business Rules:
    - BR-207: Approved verification documents cannot be deleted.
    """

    # CASCADE: Documents uploaded by a shelter cannot exist independently of that shelter organization.
    shelter = models.ForeignKey(
        "shelters.Shelter",
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("shelter"),
    )
    # SET_NULL: Preserves uploaded legal documents on shelter profile even if a specific verification workflow object is reset.
    verification = models.ForeignKey(
        "shelters.ShelterVerification",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
        verbose_name=_("associated verification workflow"),
    )
    document_type = models.CharField(
        _("document type"),
        max_length=50,
        choices=DocumentType.choices,
        db_index=True,
    )
    file = models.FileField(
        _("document file"),
        upload_to="shelters/documents/%Y/%m/",
        validators=[validate_document_file_size, validate_document_mime_type],
    )
    file_name = models.CharField(_("original file name"), max_length=255)
    file_size = models.PositiveIntegerField(
        _("file size in bytes"), help_text=_("File size in bytes")
    )
    mime_type = models.CharField(_("MIME type"), max_length=100, blank=True, default="")

    status = models.CharField(
        _("document status"),
        max_length=30,
        choices=DocumentStatus.choices,
        default=DocumentStatus.PENDING,
        db_index=True,
    )
    rejection_reason = models.TextField(_("rejection reason"), blank=True, default="")

    # SET_NULL: Preserves uploaded document audit trail even if uploading user's account is removed.
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_documents",
        verbose_name=_("uploaded by user"),
    )
    # SET_NULL: Preserves staff verification audit log even if verifying staff user account is removed.
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_documents",
        verbose_name=_("verified by staff user"),
    )

    class Meta:
        verbose_name = _("shelter document")
        verbose_name_plural = _("shelter documents")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["shelter", "document_type"]),
            models.Index(fields=["verification", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.get_document_type_display()} - {self.shelter.name}"

    @property
    def is_approved(self) -> bool:
        """Returns True if the document has been approved by reviewer."""
        return self.status == DocumentStatus.APPROVED

    @property
    def is_deletable(self) -> bool:
        """
        Business Rule BR-207:
        Approved verification documents cannot be deleted.
        """
        return not self.is_approved

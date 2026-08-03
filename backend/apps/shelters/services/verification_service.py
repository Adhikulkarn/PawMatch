"""
Service layer for Shelter verification workflows and document management.
"""

import uuid
from typing import Any, Optional

from django.db import transaction
from django.utils import timezone

from apps.shelters.constants import (
    DocumentStatus,
    ShelterStatus,
    VerificationStatus,
)
from apps.shelters.exceptions import (
    DocumentProtectedException,
    VerificationWorkflowException,
)
from apps.shelters.models import Shelter, ShelterDocument, ShelterVerification
from apps.shelters.validators import (
    validate_document_file_size,
    validate_document_mime_type,
)


class VerificationService:
    """Service managing verification request state transitions and document workflows."""

    ALLOWED_TRANSITIONS = {
        VerificationStatus.DRAFT: [VerificationStatus.SUBMITTED],
        VerificationStatus.SUBMITTED: [
            VerificationStatus.UNDER_REVIEW,
            VerificationStatus.REJECTED,
        ],
        VerificationStatus.UNDER_REVIEW: [
            VerificationStatus.APPROVED,
            VerificationStatus.NEEDS_INFORMATION,
            VerificationStatus.REJECTED,
        ],
        VerificationStatus.NEEDS_INFORMATION: [VerificationStatus.SUBMITTED],
    }

    @classmethod
    def _validate_transition(
        cls, verification: ShelterVerification, target_status: VerificationStatus
    ) -> None:
        """Validates that target state transition is permitted by the state machine."""
        current_status = verification.status
        allowed = cls.ALLOWED_TRANSITIONS.get(current_status, [])
        if target_status not in allowed:
            raise VerificationWorkflowException(
                f"Cannot transition verification from '{current_status}' to '{target_status}'."
            )

    @classmethod
    def submit_verification(cls, verification_id: uuid.UUID) -> ShelterVerification:
        """Submits a draft or needs_information verification workflow for review."""
        try:
            verification = ShelterVerification.objects.get(id=verification_id)
        except ShelterVerification.DoesNotExist:
            raise VerificationWorkflowException("Verification request not found.")

        cls._validate_transition(verification, VerificationStatus.SUBMITTED)
        verification.status = VerificationStatus.SUBMITTED
        verification.submitted_at = timezone.now()
        verification.save(update_fields=["status", "submitted_at", "updated_at"])
        return verification

    @classmethod
    def start_review(
        cls, verification_id: uuid.UUID, reviewer_user: Any
    ) -> ShelterVerification:
        """Places a submitted verification workflow under review by authorized staff."""
        try:
            verification = ShelterVerification.objects.get(id=verification_id)
        except ShelterVerification.DoesNotExist:
            raise VerificationWorkflowException("Verification request not found.")

        cls._validate_transition(verification, VerificationStatus.UNDER_REVIEW)
        verification.status = VerificationStatus.UNDER_REVIEW
        verification.reviewed_by = reviewer_user
        verification.save(update_fields=["status", "reviewed_by", "updated_at"])
        return verification

    @classmethod
    def request_information(
        cls, verification_id: uuid.UUID, reviewer_user: Any, notes: str
    ) -> ShelterVerification:
        """Requests additional information or documents from the shelter."""
        try:
            verification = ShelterVerification.objects.get(id=verification_id)
        except ShelterVerification.DoesNotExist:
            raise VerificationWorkflowException("Verification request not found.")

        cls._validate_transition(verification, VerificationStatus.NEEDS_INFORMATION)
        verification.status = VerificationStatus.NEEDS_INFORMATION
        verification.reviewed_by = reviewer_user
        verification.reviewer_notes = notes
        verification.save(
            update_fields=["status", "reviewed_by", "reviewer_notes", "updated_at"]
        )
        return verification

    @classmethod
    def approve_verification(
        cls, verification_id: uuid.UUID, reviewer_user: Any, notes: str = ""
    ) -> ShelterVerification:
        """Approves shelter verification workflow and transitions shelter status to VERIFIED."""
        try:
            verification = ShelterVerification.objects.get(id=verification_id)
        except ShelterVerification.DoesNotExist:
            raise VerificationWorkflowException("Verification request not found.")

        cls._validate_transition(verification, VerificationStatus.APPROVED)

        with transaction.atomic():
            verification.status = VerificationStatus.APPROVED
            verification.reviewed_by = reviewer_user
            verification.reviewed_at = timezone.now()
            if notes:
                verification.reviewer_notes = notes
            verification.save()

            # Transition parent shelter operational status to VERIFIED
            shelter = verification.shelter
            shelter.status = ShelterStatus.VERIFIED
            shelter.save(update_fields=["status", "updated_at"])

            # Mark associated documents as APPROVED
            verification.documents.update(
                status=DocumentStatus.APPROVED, verified_by=reviewer_user
            )

        return verification

    @classmethod
    def reject_verification(
        cls, verification_id: uuid.UUID, reviewer_user: Any, reason: str
    ) -> ShelterVerification:
        """Rejects shelter verification workflow and updates shelter status to REJECTED."""
        try:
            verification = ShelterVerification.objects.get(id=verification_id)
        except ShelterVerification.DoesNotExist:
            raise VerificationWorkflowException("Verification request not found.")

        cls._validate_transition(verification, VerificationStatus.REJECTED)

        with transaction.atomic():
            verification.status = VerificationStatus.REJECTED
            verification.reviewed_by = reviewer_user
            verification.reviewed_at = timezone.now()
            verification.rejection_reason = reason
            verification.save()

            # Transition parent shelter operational status to REJECTED
            shelter = verification.shelter
            shelter.status = ShelterStatus.REJECTED
            shelter.save(update_fields=["status", "updated_at"])

        return verification

    # --- Document Workflow Methods ---

    @classmethod
    def attach_document(
        cls,
        shelter: Shelter,
        document_type: str,
        file: Any,
        uploaded_by: Optional[Any] = None,
        verification: Optional[ShelterVerification] = None,
    ) -> ShelterDocument:
        """Validates and attaches a verification document to a shelter."""
        validate_document_file_size(file)
        validate_document_mime_type(file)

        file_name = getattr(file, "name", "document")
        file_size = getattr(file, "size", 0)
        mime_type = getattr(file, "content_type", "")

        document = ShelterDocument.objects.create(
            shelter=shelter,
            verification=verification,
            document_type=document_type,
            file=file,
            file_name=file_name,
            file_size=file_size,
            mime_type=mime_type,
            uploaded_by=uploaded_by,
            status=DocumentStatus.PENDING,
        )
        return document

    @classmethod
    def remove_document(cls, document_id: uuid.UUID) -> None:
        """
        Removes an unapproved shelter document.

        Business Rule BR-207:
        Approved verification documents cannot be deleted.
        """
        try:
            document = ShelterDocument.objects.get(id=document_id)
        except ShelterDocument.DoesNotExist:
            raise VerificationWorkflowException("Document not found.")

        if not document.is_deletable or document.status == DocumentStatus.APPROVED:
            raise DocumentProtectedException(
                "Approved verification documents cannot be deleted (BR-207)."
            )

        if document.file:
            document.file.delete(save=False)
        document.delete()

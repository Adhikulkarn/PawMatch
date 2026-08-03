"""
Unit tests for VerificationService business workflows and document management in PawMatch.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.shelters.constants import (
    DocumentStatus,
    DocumentType,
    ShelterStatus,
    VerificationStatus,
)
from apps.shelters.exceptions import (
    DocumentProtectedException,
    VerificationWorkflowException,
)
from apps.shelters.models import ShelterDocument, ShelterVerification
from apps.shelters.services import ShelterService, VerificationService

User = get_user_model()


@pytest.mark.django_db
class TestVerificationService(TestCase):
    """Test suite for VerificationService state machine transitions and document management."""

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@vservice.org",
            first_name="Owner",
            last_name="User",
            password="Password123!",
        )
        self.reviewer = User.objects.create_user(
            email="staff@pawmatch.com",
            first_name="Staff",
            last_name="Reviewer",
            password="Password123!",
            is_staff=True,
        )
        self.shelter = ShelterService.create_shelter(
            user=self.owner,
            name="Verification Test Shelter",
            email="info@vtest.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )
        self.verification = ShelterVerification.objects.get(shelter=self.shelter)

    def test_full_verification_approval_workflow(self):
        """Tests complete valid transition path: DRAFT -> SUBMITTED -> UNDER_REVIEW -> APPROVED."""
        assert self.verification.status == VerificationStatus.DRAFT

        # 1. Submit verification
        v1 = VerificationService.submit_verification(self.verification.id)
        assert v1.status == VerificationStatus.SUBMITTED
        assert v1.submitted_at is not None

        # 2. Start review
        v2 = VerificationService.start_review(v1.id, self.reviewer)
        assert v2.status == VerificationStatus.UNDER_REVIEW
        assert v2.reviewed_by == self.reviewer

        # 3. Approve verification
        v3 = VerificationService.approve_verification(
            v2.id, self.reviewer, notes="All verified"
        )
        assert v3.status == VerificationStatus.APPROVED
        assert v3.reviewed_at is not None

        # Parent shelter status must update to VERIFIED
        self.shelter.refresh_from_db()
        assert self.shelter.status == ShelterStatus.VERIFIED
        assert self.shelter.is_verified is True

    def test_verification_request_information_workflow(self):
        """Tests alternative path: SUBMITTED -> UNDER_REVIEW -> NEEDS_INFORMATION -> SUBMITTED."""
        VerificationService.submit_verification(self.verification.id)
        VerificationService.start_review(self.verification.id, self.reviewer)

        v_needs = VerificationService.request_information(
            self.verification.id, self.reviewer, notes="Missing NGO license"
        )
        assert v_needs.status == VerificationStatus.NEEDS_INFORMATION

        # Resubmit from NEEDS_INFORMATION
        v_resubmitted = VerificationService.submit_verification(self.verification.id)
        assert v_resubmitted.status == VerificationStatus.SUBMITTED

    def test_verification_rejection_workflow(self):
        """Tests rejection transition updating shelter status to REJECTED."""
        VerificationService.submit_verification(self.verification.id)
        VerificationService.start_review(self.verification.id, self.reviewer)

        v_rejected = VerificationService.reject_verification(
            self.verification.id, self.reviewer, reason="Fraudulent tax ID"
        )
        assert v_rejected.status == VerificationStatus.REJECTED
        assert v_rejected.rejection_reason == "Fraudulent tax ID"

        self.shelter.refresh_from_db()
        assert self.shelter.status == ShelterStatus.REJECTED

    def test_invalid_state_transition_raises_exception(self):
        """Tests that attempting an illegal state transition (DRAFT -> APPROVED directly) raises exception."""
        with pytest.raises(
            VerificationWorkflowException, match="Cannot transition verification"
        ):
            VerificationService.approve_verification(
                self.verification.id, self.reviewer
            )

    def test_attach_and_remove_document_workflow(self):
        """Tests document attachment and removal validation."""
        file = SimpleUploadedFile(
            "cert.pdf", b"pdf content", content_type="application/pdf"
        )
        doc = VerificationService.attach_document(
            shelter=self.shelter,
            document_type=DocumentType.REGISTRATION_CERTIFICATE,
            file=file,
            uploaded_by=self.owner,
            verification=self.verification,
        )

        assert doc.id is not None
        assert doc.status == DocumentStatus.PENDING

        # Remove unapproved document -> succeeds
        VerificationService.remove_document(doc.id)
        assert ShelterDocument.objects.filter(id=doc.id).exists() is False

    def test_approved_document_cannot_be_removed(self):
        """Tests BR-207: Approved verification documents cannot be removed."""
        file = SimpleUploadedFile(
            "license.pdf", b"pdf content", content_type="application/pdf"
        )
        doc = VerificationService.attach_document(
            shelter=self.shelter,
            document_type=DocumentType.GOVERNMENT_LICENSE,
            file=file,
            uploaded_by=self.owner,
        )
        doc.status = DocumentStatus.APPROVED
        doc.save()

        with pytest.raises(
            DocumentProtectedException,
            match="Approved verification documents cannot be deleted",
        ):
            VerificationService.remove_document(doc.id)

"""
Unit tests for the ShelterDocument entity in PawMatch.
"""

import uuid

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.shelters.constants import DocumentStatus, DocumentType
from apps.shelters.models import Shelter, ShelterDocument, ShelterVerification

User = get_user_model()


@pytest.mark.django_db
class TestShelterDocumentModel(TestCase):
    """Test suite for ShelterDocument creation, relationships, and deletion constraints."""

    def setUp(self):
        self.uploader = User.objects.create_user(
            email="uploader@shelter.org",
            first_name="Doc",
            last_name="Uploader",
            password="Password123!",
        )
        self.shelter = Shelter.objects.create(
            name="Document Test Shelter",
            slug="doc-test-shelter",
            email="info@doctest.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )
        self.verification = ShelterVerification.objects.create(
            shelter=self.shelter,
        )

    def test_create_shelter_document_successful(self):
        """Tests uploading a legal verification document for a shelter."""
        sample_file = SimpleUploadedFile(
            "cert.pdf", b"pdf content", content_type="application/pdf"
        )

        doc = ShelterDocument.objects.create(
            shelter=self.shelter,
            verification=self.verification,
            document_type=DocumentType.REGISTRATION_CERTIFICATE,
            file=sample_file,
            file_name="cert.pdf",
            file_size=11,
            mime_type="application/pdf",
            uploaded_by=self.uploader,
        )

        assert isinstance(doc.id, uuid.UUID)
        assert doc.shelter == self.shelter
        assert doc.verification == self.verification
        assert doc.document_type == DocumentType.REGISTRATION_CERTIFICATE
        assert doc.status == DocumentStatus.PENDING
        assert doc.uploaded_by == self.uploader
        assert doc.is_approved is False
        assert doc.is_deletable is True
        assert "Registration Certificate" in str(doc)

    def test_document_is_deletable_property_for_approved_document(self):
        """Tests business rule BR-207: Approved verification documents cannot be deleted."""
        sample_file = SimpleUploadedFile(
            "license.pdf", b"pdf content", content_type="application/pdf"
        )
        doc = ShelterDocument.objects.create(
            shelter=self.shelter,
            document_type=DocumentType.GOVERNMENT_LICENSE,
            file=sample_file,
            file_name="license.pdf",
            file_size=11,
            status=DocumentStatus.APPROVED,
        )

        assert doc.is_approved is True
        assert doc.is_deletable is False

    def test_user_set_null_on_uploader_deletion(self):
        """Tests that deleting uploader user sets uploaded_by to NULL (SET_NULL)."""
        sample_file = SimpleUploadedFile(
            "ngo.pdf", b"pdf content", content_type="application/pdf"
        )
        doc = ShelterDocument.objects.create(
            shelter=self.shelter,
            document_type=DocumentType.NGO_CERTIFICATE,
            file=sample_file,
            file_name="ngo.pdf",
            file_size=11,
            uploaded_by=self.uploader,
        )

        assert doc.uploaded_by == self.uploader
        self.uploader.delete()
        doc.refresh_from_db()
        assert doc.uploaded_by is None

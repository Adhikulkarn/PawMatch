"""
API integration tests for Shelter Document attachment and deletion endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from apps.shelters.constants import DocumentStatus, DocumentType
from apps.shelters.models import ShelterDocument
from apps.shelters.services import ShelterService, VerificationService

User = get_user_model()


@pytest.mark.django_db
class TestDocumentAPI(APITestCase):
    """Test suite for shelter document REST endpoints."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="docuser@shelter.org",
            first_name="Doc",
            last_name="User",
            password="Password123!",
        )
        self.client.force_authenticate(user=self.user)
        self.shelter = ShelterService.create_shelter(
            user=self.user,
            name="Document API Shelter",
            email="info@docapi.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

    def test_attach_and_list_documents_api(self):
        """Tests uploading a document via POST /api/v1/shelters/{id}/documents/ and listing it via GET."""
        pdf_file = SimpleUploadedFile(
            "license.pdf", b"pdf binary content", content_type="application/pdf"
        )
        url_attach = f"/api/v1/shelters/{self.shelter.id}/documents/"
        payload = {
            "document_type": DocumentType.GOVERNMENT_LICENSE,
            "file": pdf_file,
        }
        response = self.client.post(url_attach, data=payload, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        doc_data = response.json()["data"]
        assert doc_data["document_type"] == DocumentType.GOVERNMENT_LICENSE
        doc_id = doc_data["id"]

        # List documents
        resp_list = self.client.get(url_attach)
        assert resp_list.status_code == status.HTTP_200_OK
        assert len(resp_list.json()["data"]) == 1

        # Delete unapproved document
        url_delete = f"/api/v1/shelters/documents/{doc_id}/"
        resp_del = self.client.delete(url_delete)
        assert resp_del.status_code == status.HTTP_200_OK
        assert ShelterDocument.objects.filter(id=doc_id).exists() is False

    def test_delete_approved_document_api_fails(self):
        """Tests DELETE /api/v1/shelters/documents/{id}/ fails for approved document (BR-207)."""
        file = SimpleUploadedFile(
            "cert.pdf", b"pdf content", content_type="application/pdf"
        )
        doc = VerificationService.attach_document(
            shelter=self.shelter,
            document_type=DocumentType.REGISTRATION_CERTIFICATE,
            file=file,
        )
        doc.status = DocumentStatus.APPROVED
        doc.save()

        url_delete = f"/api/v1/shelters/documents/{doc.id}/"
        response = self.client.delete(url_delete)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            "Approved verification documents cannot be deleted"
            in response.json()["message"]
        )

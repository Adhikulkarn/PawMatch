"""
API integration tests for Shelter Verification workflow state machine endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.shelters.constants import ShelterStatus, VerificationStatus
from apps.shelters.services import ShelterService

User = get_user_model()


@pytest.mark.django_db
class TestVerificationAPI(APITestCase):
    """Test suite for shelter verification workflow REST endpoints."""

    def setUp(self):
        self.owner = User.objects.create_user(
            email="vowner@shelter.org",
            first_name="Owner",
            last_name="Verification",
            password="Password123!",
        )
        self.reviewer = User.objects.create_user(
            email="staffreviewer@pawmatch.com",
            first_name="Staff",
            last_name="Reviewer",
            password="Password123!",
            is_staff=True,
        )
        self.shelter = ShelterService.create_shelter(
            user=self.owner,
            name="Verification API Shelter",
            email="info@vapi.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )
        self.client.force_authenticate(user=self.owner)

    def test_full_verification_api_workflow(self):
        """Tests complete API verification workflow: submit -> start-review -> request-info -> submit -> approve."""
        # 1. Submit verification
        url_submit = f"/api/v1/shelters/{self.shelter.id}/verification/submit/"
        resp1 = self.client.post(url_submit)
        assert resp1.status_code == status.HTTP_200_OK
        assert resp1.json()["data"]["status"] == VerificationStatus.SUBMITTED

        # 2. Start review (staff user)
        self.client.force_authenticate(user=self.reviewer)
        url_review = f"/api/v1/shelters/{self.shelter.id}/verification/start-review/"
        resp2 = self.client.post(url_review)
        assert resp2.status_code == status.HTTP_200_OK
        assert resp2.json()["data"]["status"] == VerificationStatus.UNDER_REVIEW

        # 3. Request Information
        url_req_info = (
            f"/api/v1/shelters/{self.shelter.id}/verification/request-information/"
        )
        resp3 = self.client.post(
            url_req_info, data={"notes": "Please upload 501c3 proof"}, format="json"
        )
        assert resp3.status_code == status.HTTP_200_OK
        assert resp3.json()["data"]["status"] == VerificationStatus.NEEDS_INFORMATION

        # 4. Resubmit
        self.client.force_authenticate(user=self.owner)
        resp4 = self.client.post(url_submit)
        assert resp4.status_code == status.HTTP_200_OK
        assert resp4.json()["data"]["status"] == VerificationStatus.SUBMITTED

        # 5. Start review & Approve
        self.client.force_authenticate(user=self.reviewer)
        self.client.post(url_review)
        url_approve = f"/api/v1/shelters/{self.shelter.id}/verification/approve/"
        resp5 = self.client.post(url_approve, data={"notes": "Approved"}, format="json")
        assert resp5.status_code == status.HTTP_200_OK
        assert resp5.json()["data"]["status"] == VerificationStatus.APPROVED

        self.shelter.refresh_from_db()
        assert self.shelter.status == ShelterStatus.VERIFIED

    def test_reject_verification_api(self):
        """Tests rejecting verification workflow via API."""
        url_submit = f"/api/v1/shelters/{self.shelter.id}/verification/submit/"
        self.client.post(url_submit)

        self.client.force_authenticate(user=self.reviewer)
        url_reject = f"/api/v1/shelters/{self.shelter.id}/verification/reject/"
        resp = self.client.post(
            url_reject, data={"reason": "Invalid registration number"}, format="json"
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["data"]["status"] == VerificationStatus.REJECTED

        self.shelter.refresh_from_db()
        assert self.shelter.status == ShelterStatus.UNVERIFIED

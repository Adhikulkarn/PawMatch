"""
API integration tests for Shelter Invitation REST endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.shelters.constants import InvitationStatus, ShelterMemberRole
from apps.shelters.services import InvitationService, ShelterService

User = get_user_model()


@pytest.mark.django_db
class TestInvitationAPI(APITestCase):
    """Test suite for shelter invitation REST endpoints."""

    def setUp(self):
        self.inviter = User.objects.create_user(
            email="inviter@shelter.org",
            first_name="Inviter",
            last_name="User",
            password="Password123!",
        )
        self.acceptor = User.objects.create_user(
            email="acceptor@example.com",
            first_name="Acceptor",
            last_name="User",
            password="Password123!",
        )
        self.client.force_authenticate(user=self.inviter)
        self.shelter = ShelterService.create_shelter(
            user=self.inviter,
            name="Invitation API Shelter",
            email="info@invapi.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

    def test_create_list_accept_invitation_api_workflow(self):
        """Tests POST invitation -> GET list -> POST accept workflow via API."""
        url_inv = f"/api/v1/shelters/{self.shelter.id}/invitations/"
        payload = {
            "email": "acceptor@example.com",
            "role": ShelterMemberRole.STAFF,
        }
        response = self.client.post(url_inv, data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        inv_data = response.json()["data"]
        token = inv_data["token"]

        # List invitations
        resp_list = self.client.get(url_inv)
        assert resp_list.status_code == status.HTTP_200_OK
        assert len(resp_list.json()["data"]) == 1

        # Accept invitation
        self.client.force_authenticate(user=self.acceptor)
        url_accept = "/api/v1/shelters/invitations/accept/"
        resp_accept = self.client.post(url_accept, data={"token": token}, format="json")
        assert resp_accept.status_code == status.HTTP_200_OK
        assert resp_accept.json()["data"]["role"] == ShelterMemberRole.STAFF

    def test_revoke_invitation_api(self):
        """Tests revoking a pending invitation via POST /api/v1/shelters/invitations/revoke/."""
        invitation = InvitationService.create_invitation(
            shelter=self.shelter,
            email="to_revoke@example.com",
            role=ShelterMemberRole.VOLUNTEER,
            invited_by=self.inviter,
        )

        url_revoke = "/api/v1/shelters/invitations/revoke/"
        response = self.client.post(
            url_revoke, data={"invitation_id": str(invitation.id)}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["status"] == InvitationStatus.REVOKED

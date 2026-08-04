"""
API integration tests for Shelter Member REST endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.shelters.constants import ShelterMemberRole
from apps.shelters.models import ShelterMember
from apps.shelters.services import ShelterService

User = get_user_model()


@pytest.mark.django_db
class TestMemberAPI(APITestCase):
    """Test suite for shelter member REST endpoints."""

    def setUp(self):
        self.owner = User.objects.create_user(
            email="mowner@shelter.org",
            first_name="Member",
            last_name="Owner",
            password="Password123!",
        )
        self.staff_user = User.objects.create_user(
            email="mstaff@shelter.org",
            first_name="Staff",
            last_name="User",
            password="Password123!",
        )
        self.client.force_authenticate(user=self.owner)
        self.shelter = ShelterService.create_shelter(
            user=self.owner,
            name="Member API Shelter",
            email="info@memberapi.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )
        self.owner_member = ShelterMember.objects.get(
            shelter=self.shelter, user=self.owner
        )

    def test_add_and_list_members_api(self):
        """Tests POST /api/v1/shelters/{id}/members/ and GET /api/v1/shelters/{id}/members/."""
        url_members = f"/api/v1/shelters/{self.shelter.id}/members/"
        payload = {
            "user_id": str(self.staff_user.id),
            "role": ShelterMemberRole.STAFF,
        }
        response = self.client.post(url_members, data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        member_id = response.json()["data"]["id"]

        # List members
        resp_list = self.client.get(url_members)
        assert resp_list.status_code == status.HTTP_200_OK
        assert len(resp_list.json()["data"]) == 2

        # Update member role
        url_detail = f"/api/v1/shelters/members/{member_id}/"
        resp_patch = self.client.patch(
            url_detail, data={"role": ShelterMemberRole.MANAGER}, format="json"
        )
        assert resp_patch.status_code == status.HTTP_200_OK
        assert resp_patch.json()["data"]["role"] == ShelterMemberRole.MANAGER

        # Delete added member
        resp_del = self.client.delete(url_detail)
        assert resp_del.status_code == status.HTTP_200_OK
        assert ShelterMember.objects.filter(id=member_id).exists() is False

    def test_remove_last_owner_api_fails(self):
        """Tests DELETE /api/v1/shelters/members/{id}/ fails for last owner (BR-203)."""
        url_detail = f"/api/v1/shelters/members/{self.owner_member.id}/"
        response = self.client.delete(url_detail)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Cannot remove the last remaining OWNER" in response.json()["message"]

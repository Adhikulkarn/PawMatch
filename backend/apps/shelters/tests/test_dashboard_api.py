"""
API integration tests for Shelter Dashboard endpoint (GET /api/v1/shelters/dashboard/).
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.shelters.constants import VerificationStatus
from apps.shelters.services import ShelterService

User = get_user_model()


@pytest.mark.django_db
class TestShelterDashboardAPI(APITestCase):
    """Test suite for shelter dashboard REST endpoint."""

    def setUp(self):
        self.owner = User.objects.create_user(
            email="dashuser@shelter.org",
            first_name="Dash",
            last_name="User",
            password="Password123!",
        )
        self.client.force_authenticate(user=self.owner)
        self.shelter = ShelterService.create_shelter(
            user=self.owner,
            name="Dashboard API Shelter",
            email="info@dashapi.org",
            phone_number="123456",
            address_line1="100 Dash St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

    def test_get_shelter_dashboard_endpoint_success(self):
        """Tests GET /api/v1/shelters/dashboard/ returns required contract fields."""
        response = self.client.get("/api/v1/shelters/dashboard/")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()["data"]
        assert data["organization_name"] == "Dashboard API Shelter"
        assert data["verification_status"] == VerificationStatus.DRAFT
        assert data["total_pets"] == 0
        assert data["available_pets"] == 0
        assert data["adopted_pets"] == 0
        assert data["pending_applications"] == 0
        assert data["recent_notifications"] == []

    def test_get_shelter_dashboard_unauthenticated_fails(self):
        """Tests GET /api/v1/shelters/dashboard/ requires authentication."""
        self.client.logout()
        response = self.client.get("/api/v1/shelters/dashboard/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

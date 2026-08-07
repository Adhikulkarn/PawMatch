"""
API integration tests for Shelter organization CRUD, search, filtering, and register/me endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.shelters.services import ShelterService

User = get_user_model()


@pytest.mark.django_db
class TestShelterAPI(APITestCase):
    """Test suite for /api/v1/shelters/ REST endpoints."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="apiowner@shelter.org",
            first_name="API",
            last_name="Owner",
            password="Password123!",
        )
        self.client.force_authenticate(user=self.user)
        self.shelter = ShelterService.create_shelter(
            user=self.user,
            name="Austin Rescue Center",
            email="info@austinrescue.org",
            phone_number="5125550199",
            address_line1="100 Rescue Rd",
            city="Austin",
            state="TX",
            postal_code="78702",
        )

    def test_list_shelters_endpoint(self):
        """Tests GET /api/v1/shelters/ returns paginated shelter listings."""
        response = self.client.get("/api/v1/shelters/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "count" in data
        assert data["count"] >= 1
        assert "results" in data
        assert data["results"][0]["name"] == "Austin Rescue Center"

    def test_filter_and_search_shelters(self):
        """Tests searching by name and filtering by city and status."""
        response = self.client.get(
            "/api/v1/shelters/?search=Austin&city=Austin&status=unverified"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1

    def test_create_shelter_endpoint(self):
        """Tests POST /api/v1/shelters/ onboards a new shelter."""
        new_user = User.objects.create_user(
            email="newcreator@shelter.org",
            first_name="New",
            last_name="Creator",
            password="Password123!",
        )
        self.client.force_authenticate(user=new_user)
        payload = {
            "name": "Dallas Animal Sanctuary",
            "email": "info@dallas.org",
            "phone_number": "2145550100",
            "address_line1": "500 Sanctuary Way",
            "city": "Dallas",
            "state": "TX",
            "postal_code": "75201",
        }
        response = self.client.post("/api/v1/shelters/", data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        res_data = response.json()
        assert res_data["success"] is True
        assert res_data["data"]["name"] == "Dallas Animal Sanctuary"
        assert res_data["data"]["slug"] == "dallas-animal-sanctuary"

    def test_register_shelter_top_level_endpoint(self):
        """Tests POST /api/v1/shelters/register/ onboards a shelter."""
        reg_user = User.objects.create_user(
            email="registeruser@shelter.org",
            first_name="Reg",
            last_name="User",
            password="Password123!",
        )
        self.client.force_authenticate(user=reg_user)
        payload = {
            "name": "Houston Paws Rescue",
            "email": "contact@houstonpaws.org",
            "phone_number": "7135550199",
            "address_line1": "700 Rescue Blvd",
            "city": "Houston",
            "state": "TX",
            "postal_code": "77001",
        }
        response = self.client.post(
            "/api/v1/shelters/register/", data=payload, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        res_data = response.json()
        assert res_data["success"] is True
        assert res_data["data"]["name"] == "Houston Paws Rescue"

    def test_shelter_me_get_and_patch_endpoints(self):
        """Tests GET and PATCH /api/v1/shelters/me/ for current user's shelter."""
        response = self.client.get("/api/v1/shelters/me/")
        assert response.status_code == status.HTTP_200_OK
        res_data = response.json()
        assert res_data["data"]["name"] == "Austin Rescue Center"

        patch_payload = {"phone_number": "5128889999"}
        patch_resp = self.client.patch(
            "/api/v1/shelters/me/", data=patch_payload, format="json"
        )
        assert patch_resp.status_code == status.HTTP_200_OK
        assert patch_resp.json()["data"]["phone_number"] == "5128889999"

    def test_retrieve_shelter_endpoint(self):
        """Tests GET /api/v1/shelters/{id}/ returns shelter details."""
        url = f"/api/v1/shelters/{self.shelter.id}/"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        res_data = response.json()
        assert res_data["data"]["id"] == str(self.shelter.id)

    def test_partial_update_shelter_endpoint(self):
        """Tests PATCH /api/v1/shelters/{id}/ updates profile fields."""
        url = f"/api/v1/shelters/{self.shelter.id}/"
        payload = {
            "phone_number": "5129990000",
            "description": "Updated shelter description.",
        }
        response = self.client.patch(url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        res_data = response.json()
        assert res_data["data"]["phone_number"] == "5129990000"
        assert res_data["data"]["description"] == "Updated shelter description."

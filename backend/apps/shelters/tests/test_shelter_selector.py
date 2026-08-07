"""
Unit tests for Shelter domain selector queries in PawMatch.
"""

import pytest
from django.test import TestCase

from apps.shelters.constants import ShelterStatus
from apps.shelters.models import Shelter
from apps.shelters.selectors import (
    get_shelter_by_id,
    get_shelter_by_slug,
    get_shelters_by_status,
    list_all_shelters,
    list_verified_shelters,
    search_shelters,
)


@pytest.mark.django_db
class TestShelterSelector(TestCase):
    """Test suite for shelter selector queries and filters."""

    def setUp(self):
        self.shelter = Shelter.objects.create(
            name="Capital Pet Rescue",
            slug="capital-pet-rescue",
            legal_name="Capital Rescue Organization",
            email="info@capitalrescue.org",
            city="Austin",
            state="TX",
            status=ShelterStatus.VERIFIED,
            is_active=True,
        )

    def test_get_shelter_by_id_and_slug(self):
        by_id = get_shelter_by_id(self.shelter.id)
        assert by_id == self.shelter

        by_slug = get_shelter_by_slug("capital-pet-rescue")
        assert by_slug == self.shelter

    def test_list_verified_shelters(self):
        unverified = Shelter.objects.create(
            name="Unverified Shelter",
            slug="unverified-shelter",
            email="info@unverified.org",
            city="Dallas",
            state="TX",
            status=ShelterStatus.UNVERIFIED,
        )

        verified_qs = list_verified_shelters()
        assert self.shelter in verified_qs
        assert unverified not in verified_qs

    def test_list_all_shelters_filtering(self):
        all_qs = list_all_shelters(city="austin", state="TX")
        assert self.shelter in all_qs

        by_status = get_shelters_by_status(ShelterStatus.VERIFIED)
        assert self.shelter in by_status

    def test_search_shelters(self):
        search_res = search_shelters("Capital")
        assert self.shelter in search_res

"""
Unit tests for the Shelter entity in PawMatch.
"""

import uuid
from decimal import Decimal

import pytest
from django.db import IntegrityError
from django.test import TestCase

from apps.shelters.constants import ShelterStatus
from apps.shelters.models import Shelter


@pytest.mark.django_db
class TestShelterModel(TestCase):
    """Test suite for Shelter model creation, defaults, constraints, and helper properties."""

    def test_create_shelter_successful(self):
        """Tests creating a Shelter with valid required and optional fields."""
        shelter = Shelter.objects.create(
            name="Happy Paws Rescue",
            slug="happy-paws-rescue",
            email="contact@happypaws.org",
            phone_number="+15551234567",
            address_line1="123 Rescue Way",
            city="Austin",
            state="TX",
            postal_code="78701",
            country="USA",
            latitude=Decimal("30.267200"),
            longitude=Decimal("-97.743100"),
        )

        assert isinstance(shelter.id, uuid.UUID)
        assert shelter.name == "Happy Paws Rescue"
        assert shelter.slug == "happy-paws-rescue"
        assert shelter.status == ShelterStatus.UNVERIFIED
        assert shelter.is_active is True
        assert shelter.is_deleted is False
        assert str(shelter) == "Happy Paws Rescue"
        assert shelter.created_at is not None
        assert shelter.updated_at is not None

    def test_shelter_unique_slug_constraint(self):
        """Tests that creating a shelter with a duplicate slug raises IntegrityError."""
        Shelter.objects.create(
            name="Shelter One",
            slug="duplicate-slug",
            email="one@shelter.org",
            phone_number="123",
            address_line1="Line 1",
            city="City",
            state="ST",
            postal_code="12345",
        )

        with pytest.raises(IntegrityError):
            Shelter.objects.create(
                name="Shelter Two",
                slug="duplicate-slug",
                email="two@shelter.org",
                phone_number="456",
                address_line1="Line 2",
                city="City",
                state="ST",
                postal_code="12345",
            )

    def test_shelter_is_verified_property(self):
        """Tests is_verified helper property across status transitions."""
        shelter = Shelter.objects.create(
            name="Verification Test Shelter",
            slug="verification-test-shelter",
            email="vtest@shelter.org",
            phone_number="123",
            address_line1="Line 1",
            city="City",
            state="ST",
            postal_code="12345",
            status=ShelterStatus.UNVERIFIED,
        )

        assert shelter.is_verified is False

        shelter.status = ShelterStatus.VERIFIED
        shelter.save()
        shelter.refresh_from_db()

        assert shelter.is_verified is True

    def test_shelter_can_publish_pets_property(self):
        """Tests business rule BR-202 on can_publish_pets property."""
        shelter = Shelter.objects.create(
            name="Publish Test Shelter",
            slug="publish-test-shelter",
            email="ptest@shelter.org",
            phone_number="123",
            address_line1="Line 1",
            city="City",
            state="ST",
            postal_code="12345",
            status=ShelterStatus.UNVERIFIED,
            is_active=True,
        )

        assert shelter.can_publish_pets is False

        # Status becomes VERIFIED -> can_publish_pets is True
        shelter.status = ShelterStatus.VERIFIED
        shelter.save()
        assert shelter.can_publish_pets is True

        # Deactivated shelter -> cannot publish pets
        shelter.is_active = False
        shelter.save()
        assert shelter.can_publish_pets is False

        # Re-activate and soft-delete shelter -> cannot publish pets
        shelter.is_active = True
        shelter.soft_delete()
        assert shelter.can_publish_pets is False

    def test_shelter_soft_delete_and_restore(self):
        """Tests soft delete and restoration capabilities on Shelter entity."""
        shelter = Shelter.objects.create(
            name="Soft Delete Shelter",
            slug="soft-delete-shelter",
            email="sd@shelter.org",
            phone_number="123",
            address_line1="Line 1",
            city="City",
            state="ST",
            postal_code="12345",
        )

        assert shelter.is_deleted is False
        assert shelter.deleted_at is None

        shelter.soft_delete()
        shelter.refresh_from_db()

        assert shelter.is_deleted is True
        assert shelter.deleted_at is not None

        shelter.restore()
        shelter.refresh_from_db()

        assert shelter.is_deleted is False
        assert shelter.deleted_at is None

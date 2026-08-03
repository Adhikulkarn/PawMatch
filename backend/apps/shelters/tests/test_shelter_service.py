"""
Unit tests for ShelterService business workflows in PawMatch.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.shelters.constants import ShelterMemberRole, ShelterStatus, VerificationStatus
from apps.shelters.exceptions import MemberAlreadyExistsException
from apps.shelters.models import ShelterMember, ShelterVerification
from apps.shelters.services import ShelterService

User = get_user_model()


@pytest.mark.django_db
class TestShelterService(TestCase):
    """Test suite for ShelterService creation, updates, and state transitions."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@shelterservice.org",
            first_name="Owner",
            last_name="User",
            password="Password123!",
        )

    def test_create_shelter_workflow_successful(self):
        """Tests end-to-end create_shelter workflow initializing shelter, owner member, and draft verification."""
        shelter = ShelterService.create_shelter(
            user=self.user,
            name="Austin Animal Rescue",
            email="info@austinrescue.org",
            phone_number="5125550199",
            address_line1="100 Rescue Rd",
            city="Austin",
            state="TX",
            postal_code="78702",
        )

        assert shelter.id is not None
        assert shelter.name == "Austin Animal Rescue"
        assert shelter.slug == "austin-animal-rescue"
        assert shelter.status == ShelterStatus.UNVERIFIED

        # Check owner membership
        members = ShelterMember.objects.filter(shelter=shelter)
        assert members.count() == 1
        owner_member = members.first()
        assert owner_member.user == self.user
        assert owner_member.role == ShelterMemberRole.OWNER

        # Check initialized draft verification
        verifications = ShelterVerification.objects.filter(shelter=shelter)
        assert verifications.count() == 1
        assert verifications.first().status == VerificationStatus.DRAFT

    def test_create_shelter_duplicate_user_raises_exception(self):
        """Tests BR-204: User belonging to an active shelter cannot create/onboard another shelter."""
        ShelterService.create_shelter(
            user=self.user,
            name="First Shelter",
            email="first@shelter.org",
            phone_number="123",
            address_line1="Line 1",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

        with pytest.raises(
            MemberAlreadyExistsException, match="already belongs to an active shelter"
        ):
            ShelterService.create_shelter(
                user=self.user,
                name="Second Shelter",
                email="second@shelter.org",
                phone_number="456",
                address_line1="Line 2",
                city="Austin",
                state="TX",
                postal_code="78701",
            )

    def test_update_shelter_profile_and_slug_regeneration(self):
        """Tests updating shelter profile and automatic slug regeneration on name change."""
        shelter = ShelterService.create_shelter(
            user=self.user,
            name="Old Shelter Name",
            email="info@old.org",
            phone_number="123",
            address_line1="Line 1",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

        assert shelter.slug == "old-shelter-name"

        updated = ShelterService.update_shelter(
            shelter.id, name="New Shelter Name", phone_number="999999"
        )
        assert updated.name == "New Shelter Name"
        assert updated.slug == "new-shelter-name"
        assert updated.phone_number == "999999"

    def test_archive_and_suspend_shelter_lifecycle(self):
        """Tests archiving and suspending shelter operational status."""
        shelter = ShelterService.create_shelter(
            user=self.user,
            name="Lifecycle Shelter",
            email="info@life.org",
            phone_number="123",
            address_line1="Line 1",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

        suspended = ShelterService.suspend_shelter(shelter.id)
        assert suspended.status == ShelterStatus.SUSPENDED
        assert suspended.is_active is False

        archived = ShelterService.archive_shelter(shelter.id)
        assert archived.status == ShelterStatus.ARCHIVED
        assert archived.is_active is False

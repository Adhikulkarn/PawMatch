"""
Unit tests for the ShelterMember entity in PawMatch.
"""

import uuid

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from apps.shelters.constants import ShelterMemberRole
from apps.shelters.models import Shelter, ShelterMember

User = get_user_model()


@pytest.mark.django_db
class TestShelterMemberModel(TestCase):
    """Test suite for ShelterMember creation, relationships, constraints, and roles."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="member@shelter.org",
            first_name="Member",
            last_name="User",
            password="Password123!",
        )
        self.shelter = Shelter.objects.create(
            name="Member Test Shelter",
            slug="member-test-shelter",
            email="info@membershelter.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

    def test_create_shelter_member_successful(self):
        """Tests creating a ShelterMember with default role and active status."""
        member = ShelterMember.objects.create(
            shelter=self.shelter,
            user=self.user,
            role=ShelterMemberRole.OWNER,
        )

        assert isinstance(member.id, uuid.UUID)
        assert member.shelter == self.shelter
        assert member.user == self.user
        assert member.role == ShelterMemberRole.OWNER
        assert member.is_active is True
        assert member.is_owner is True
        assert member.is_manager is True
        assert f"{self.user} - {self.shelter.name}" in str(member)
        assert self.shelter.members.count() == 1
        assert self.user.shelter_memberships.count() == 1

    def test_shelter_member_unique_constraint(self):
        """Tests that duplicate membership for same (user, shelter) raises IntegrityError."""
        ShelterMember.objects.create(
            shelter=self.shelter,
            user=self.user,
            role=ShelterMemberRole.VOLUNTEER,
        )

        with pytest.raises(IntegrityError):
            ShelterMember.objects.create(
                shelter=self.shelter,
                user=self.user,
                role=ShelterMemberRole.STAFF,
            )

    def test_shelter_member_roles_and_properties(self):
        """Tests is_owner and is_manager properties across member roles."""
        staff_user = User.objects.create_user(
            email="staff@shelter.org",
            first_name="Staff",
            last_name="User",
            password="Password123!",
        )
        member = ShelterMember.objects.create(
            shelter=self.shelter,
            user=staff_user,
            role=ShelterMemberRole.STAFF,
        )

        assert member.is_owner is False
        assert member.is_manager is False

        member.role = ShelterMemberRole.MANAGER
        member.save()

        assert member.is_owner is False
        assert member.is_manager is True

    def test_shelter_cascade_deletion(self):
        """Tests that deleting a shelter cascades and removes its members."""
        ShelterMember.objects.create(
            shelter=self.shelter,
            user=self.user,
            role=ShelterMemberRole.OWNER,
        )

        assert ShelterMember.objects.count() == 1
        self.shelter.delete()
        assert ShelterMember.objects.count() == 0

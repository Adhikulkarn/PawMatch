"""
Unit tests for MemberService business workflows and ownership safeguards in PawMatch.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.shelters.constants import ShelterMemberRole
from apps.shelters.exceptions import (
    LastOwnerRemovalException,
    MemberAlreadyExistsException,
)
from apps.shelters.models import ShelterMember
from apps.shelters.services import MemberService, ShelterService

User = get_user_model()


@pytest.mark.django_db
class TestMemberService(TestCase):
    """Test suite for MemberService operations, role changes, and ownership transfer safeguards."""

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@memberservice.org",
            first_name="Owner",
            last_name="One",
            password="Password123!",
        )
        self.new_user = User.objects.create_user(
            email="newuser@memberservice.org",
            first_name="New",
            last_name="User",
            password="Password123!",
        )
        self.shelter = ShelterService.create_shelter(
            user=self.owner,
            name="Member Service Shelter",
            email="info@mservice.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )
        self.owner_member = ShelterMember.objects.get(
            shelter=self.shelter, user=self.owner
        )

    def test_add_member_workflow(self):
        """Tests adding a new member to a shelter."""
        member = MemberService.add_member(
            shelter=self.shelter,
            user=self.new_user,
            role=ShelterMemberRole.STAFF,
        )

        assert member.id is not None
        assert member.shelter == self.shelter
        assert member.user == self.new_user
        assert member.role == ShelterMemberRole.STAFF

    def test_add_member_existing_shelter_user_raises_exception(self):
        """Tests BR-204: Cannot add a user who is already a member of an active shelter."""
        with pytest.raises(
            MemberAlreadyExistsException, match="already belongs to an active shelter"
        ):
            MemberService.add_member(
                shelter=self.shelter,
                user=self.owner,  # Already an owner of this shelter
                role=ShelterMemberRole.VOLUNTEER,
            )

    def test_remove_last_owner_raises_exception(self):
        """Tests BR-203: Removing the last remaining OWNER of a shelter raises LastOwnerRemovalException."""
        with pytest.raises(
            LastOwnerRemovalException, match="Cannot remove the last remaining OWNER"
        ):
            MemberService.remove_member(self.owner_member.id)

    def test_demote_last_owner_raises_exception(self):
        """Tests BR-203: Changing the role of the last remaining OWNER away from OWNER raises LastOwnerRemovalException."""
        with pytest.raises(
            LastOwnerRemovalException, match="Cannot demote the last remaining OWNER"
        ):
            MemberService.change_role(self.owner_member.id, ShelterMemberRole.MANAGER)

    def test_transfer_ownership_workflow(self):
        """Tests transferring shelter ownership from current owner to new owner user."""
        current_owner, new_owner = MemberService.transfer_ownership(
            shelter=self.shelter,
            current_owner_user=self.owner,
            new_owner_user=self.new_user,
        )

        # Former owner demoted to MANAGER
        current_owner.refresh_from_db()
        assert current_owner.role == ShelterMemberRole.MANAGER

        # New user promoted to OWNER
        new_owner.refresh_from_db()
        assert new_owner.role == ShelterMemberRole.OWNER
        assert new_owner.is_owner is True

        # Ensure shelter still has exactly one owner
        active_owners = ShelterMember.objects.filter(
            shelter=self.shelter, role=ShelterMemberRole.OWNER, is_active=True
        )
        assert active_owners.count() == 1
        assert active_owners.first().user == self.new_user

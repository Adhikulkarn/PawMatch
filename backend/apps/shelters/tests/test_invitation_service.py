"""
Unit tests for InvitationService business workflows in PawMatch.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.shelters.constants import InvitationStatus, ShelterMemberRole
from apps.shelters.exceptions import (
    InvitationExpiredException,
    MemberAlreadyExistsException,
    ShelterDomainException,
)
from apps.shelters.services import InvitationService, ShelterService

User = get_user_model()


@pytest.mark.django_db
class TestInvitationService(TestCase):
    """Test suite for InvitationService creation, token acceptance, and expiration."""

    def setUp(self):
        self.inviter = User.objects.create_user(
            email="manager@shelter.org",
            first_name="Manager",
            last_name="Inviter",
            password="Password123!",
        )
        self.invitee_user = User.objects.create_user(
            email="newmember@example.com",
            first_name="New",
            last_name="Member",
            password="Password123!",
        )
        self.shelter = ShelterService.create_shelter(
            user=self.inviter,
            name="Invitation Workflow Shelter",
            email="info@invworkflow.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

    def test_create_and_accept_invitation_workflow(self):
        """Tests creating an invitation and accepting it to establish shelter membership."""
        invitation = InvitationService.create_invitation(
            shelter=self.shelter,
            email="newmember@example.com",
            role=ShelterMemberRole.STAFF,
            invited_by=self.inviter,
        )

        assert invitation.status == InvitationStatus.PENDING
        assert invitation.token is not None

        # Accept invitation
        member = InvitationService.accept_invitation(
            invitation.token, self.invitee_user
        )

        assert member.shelter == self.shelter
        assert member.user == self.invitee_user
        assert member.role == ShelterMemberRole.STAFF

        invitation.refresh_from_db()
        assert invitation.status == InvitationStatus.ACCEPTED
        assert invitation.accepted_by == self.invitee_user
        assert invitation.accepted_at is not None

    def test_create_duplicate_pending_invitation_raises_exception(self):
        """Tests that creating a duplicate pending invitation for the same email raises an exception."""
        InvitationService.create_invitation(
            shelter=self.shelter,
            email="pending@example.com",
            role=ShelterMemberRole.VOLUNTEER,
            invited_by=self.inviter,
        )

        with pytest.raises(
            ShelterDomainException, match="pending invitation already exists"
        ):
            InvitationService.create_invitation(
                shelter=self.shelter,
                email="pending@example.com",
                role=ShelterMemberRole.STAFF,
                invited_by=self.inviter,
            )

    def test_accept_expired_invitation_raises_exception(self):
        """Tests BR-205: Accepting an expired invitation updates status to EXPIRED and raises InvitationExpiredException."""
        invitation = InvitationService.create_invitation(
            shelter=self.shelter,
            email="expired@example.com",
            role=ShelterMemberRole.STAFF,
            invited_by=self.inviter,
            expiry_days=-1,  # Already expired
        )

        with pytest.raises(InvitationExpiredException, match="Invitation has expired"):
            InvitationService.accept_invitation(invitation.token, self.invitee_user)

        invitation.refresh_from_db()
        assert invitation.status == InvitationStatus.EXPIRED

    def test_accept_invitation_user_already_in_shelter_raises_exception(self):
        """Tests BR-204: Accepting invitation when user already belongs to a shelter raises MemberAlreadyExistsException."""
        another_user = User.objects.create_user(
            email="busyuser@example.com",
            first_name="Busy",
            last_name="User",
            password="Password123!",
        )
        # Create a shelter for another_user
        ShelterService.create_shelter(
            user=another_user,
            name="Another Shelter",
            email="info@another.org",
            phone_number="123",
            address_line1="Line 1",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

        invitation = InvitationService.create_invitation(
            shelter=self.shelter,
            email="busyuser@example.com",
            role=ShelterMemberRole.STAFF,
            invited_by=self.inviter,
        )

        with pytest.raises(
            MemberAlreadyExistsException, match="already belongs to an active shelter"
        ):
            InvitationService.accept_invitation(invitation.token, another_user)

    def test_revoke_invitation_workflow(self):
        """Tests revoking a pending invitation."""
        invitation = InvitationService.create_invitation(
            shelter=self.shelter,
            email="revoke@example.com",
            role=ShelterMemberRole.VOLUNTEER,
            invited_by=self.inviter,
        )

        revoked = InvitationService.revoke_invitation(invitation.id)
        assert revoked.status == InvitationStatus.REVOKED
        assert revoked.responded_at is not None

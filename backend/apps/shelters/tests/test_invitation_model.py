"""
Unit tests for the ShelterInvitation entity in PawMatch.
"""

import uuid
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from apps.shelters.constants import InvitationStatus, ShelterMemberRole
from apps.shelters.models import Shelter, ShelterInvitation

User = get_user_model()


@pytest.mark.django_db
class TestShelterInvitationModel(TestCase):
    """Test suite for ShelterInvitation creation, token uniqueness, and expiration."""

    def setUp(self):
        self.inviter = User.objects.create_user(
            email="inviter@shelter.org",
            first_name="Inviter",
            last_name="Manager",
            password="Password123!",
        )
        self.shelter = Shelter.objects.create(
            name="Invitation Test Shelter",
            slug="inv-test-shelter",
            email="info@invtest.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

    def test_create_shelter_invitation_successful(self):
        """Tests creating a ShelterInvitation instance."""
        token = uuid.uuid4().hex
        invitation = ShelterInvitation.objects.create(
            shelter=self.shelter,
            email="invitee@example.com",
            role=ShelterMemberRole.STAFF,
            token=token,
            invited_by=self.inviter,
            expires_at=timezone.now() + timedelta(days=7),
        )

        assert isinstance(invitation.id, uuid.UUID)
        assert invitation.shelter == self.shelter
        assert invitation.email == "invitee@example.com"
        assert invitation.role == ShelterMemberRole.STAFF
        assert invitation.token == token
        assert invitation.status == InvitationStatus.PENDING
        assert invitation.invited_by == self.inviter
        assert invitation.accepted_by is None
        assert invitation.is_expired is False
        assert invitation.is_valid is True
        assert "invitee@example.com" in str(invitation)

    def test_unique_pending_invitation_constraint(self):
        """Tests that creating a duplicate pending invitation for same shelter and email raises IntegrityError."""
        ShelterInvitation.objects.create(
            shelter=self.shelter,
            email="duplicate@example.com",
            role=ShelterMemberRole.VOLUNTEER,
            token="token-1",
            invited_by=self.inviter,
            expires_at=timezone.now() + timedelta(days=7),
        )

        with pytest.raises(IntegrityError):
            ShelterInvitation.objects.create(
                shelter=self.shelter,
                email="duplicate@example.com",
                role=ShelterMemberRole.STAFF,
                token="token-2",
                invited_by=self.inviter,
                expires_at=timezone.now() + timedelta(days=7),
            )

    def test_invitation_expiration_property(self):
        """Tests business rule BR-205 on invitation expiration."""
        invitation = ShelterInvitation.objects.create(
            shelter=self.shelter,
            email="past@example.com",
            role=ShelterMemberRole.VOLUNTEER,
            token="token-past",
            invited_by=self.inviter,
            expires_at=timezone.now() - timedelta(hours=1),
        )

        assert invitation.is_expired is True
        assert invitation.is_valid is False

    def test_accepted_by_set_null_on_user_deletion(self):
        """Tests SET_NULL on accepted_by field when accepted user is deleted."""
        acceptor = User.objects.create_user(
            email="accepted@example.com",
            first_name="Accepted",
            last_name="User",
            password="Password123!",
        )
        invitation = ShelterInvitation.objects.create(
            shelter=self.shelter,
            email="accepted@example.com",
            role=ShelterMemberRole.STAFF,
            token="token-accepted",
            invited_by=self.inviter,
            accepted_by=acceptor,
            accepted_at=timezone.now(),
            status=InvitationStatus.ACCEPTED,
            expires_at=timezone.now() + timedelta(days=7),
        )

        assert invitation.accepted_by == acceptor
        acceptor.delete()
        invitation.refresh_from_db()
        assert invitation.accepted_by is None

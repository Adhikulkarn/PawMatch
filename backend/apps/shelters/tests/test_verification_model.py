"""
Unit tests for the ShelterVerification entity in PawMatch.
"""

import uuid

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from apps.shelters.constants import VerificationStatus
from apps.shelters.models import Shelter, ShelterVerification

User = get_user_model()


@pytest.mark.django_db
class TestShelterVerificationModel(TestCase):
    """Test suite for ShelterVerification state workflow and constraints."""

    def setUp(self):
        self.reviewer = User.objects.create_user(
            email="reviewer@pawmatch.com",
            first_name="Reviewer",
            last_name="Staff",
            password="Password123!",
            is_staff=True,
        )
        self.shelter = Shelter.objects.create(
            name="Verification Test Shelter",
            slug="vtest-shelter",
            email="info@vtest.org",
            phone_number="123456",
            address_line1="123 Main St",
            city="Austin",
            state="TX",
            postal_code="78701",
        )

    def test_create_shelter_verification_successful(self):
        """Tests creating a ShelterVerification workflow instance."""
        verification = ShelterVerification.objects.create(
            shelter=self.shelter,
            status=VerificationStatus.DRAFT,
        )

        assert isinstance(verification.id, uuid.UUID)
        assert verification.shelter == self.shelter
        assert verification.status == VerificationStatus.DRAFT
        assert verification.is_active_workflow is True
        assert verification.is_approved is False
        assert f"Verification for {self.shelter.name}" in str(verification)

    def test_unique_active_verification_constraint(self):
        """Tests that a shelter cannot have multiple active verification workflows."""
        ShelterVerification.objects.create(
            shelter=self.shelter,
            status=VerificationStatus.SUBMITTED,
            submitted_at=timezone.now(),
        )

        with pytest.raises(IntegrityError):
            ShelterVerification.objects.create(
                shelter=self.shelter,
                status=VerificationStatus.DRAFT,
            )

    def test_verification_terminal_states_allow_new_submission(self):
        """Tests that approved/rejected terminal states permit creating a new verification instance."""
        v1 = ShelterVerification.objects.create(
            shelter=self.shelter,
            status=VerificationStatus.REJECTED,
            reviewed_by=self.reviewer,
            rejection_reason="Incomplete documents",
        )
        assert v1.is_active_workflow is False

        # Creating a second verification is allowed because v1 is in REJECTED status
        v2 = ShelterVerification.objects.create(
            shelter=self.shelter,
            status=VerificationStatus.SUBMITTED,
            submitted_at=timezone.now(),
        )
        assert v2.is_active_workflow is True
        assert self.shelter.verifications.count() == 2

    def test_reviewer_set_null_on_user_deletion(self):
        """Tests that deleting reviewer user sets reviewed_by to NULL (SET_NULL)."""
        verification = ShelterVerification.objects.create(
            shelter=self.shelter,
            status=VerificationStatus.APPROVED,
            reviewed_by=self.reviewer,
            reviewed_at=timezone.now(),
        )

        assert verification.reviewed_by == self.reviewer
        self.reviewer.delete()
        verification.refresh_from_db()
        assert verification.reviewed_by is None

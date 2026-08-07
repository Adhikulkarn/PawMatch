"""
Unit tests for DashboardService metrics aggregation in PawMatch.
"""

import uuid

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.shelters.constants import (
    DocumentStatus,
    DocumentType,
    OrganizationType,
    ShelterMemberRole,
    ShelterStatus,
    VerificationStatus,
)
from apps.shelters.exceptions import ShelterNotFoundException
from apps.shelters.models import (
    Shelter,
    ShelterDocument,
    ShelterMember,
    ShelterVerification,
)
from apps.shelters.services.dashboard_service import DashboardService

User = get_user_model()


@pytest.mark.django_db
class TestDashboardService(TestCase):
    """Test suite for DashboardService shelter and system dashboard aggregations."""

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@dashboard.org",
            first_name="Owner",
            last_name="User",
            password="Password123!",
        )
        self.shelter = Shelter.objects.create(
            name="Metro Animal Shelter",
            slug="metro-animal-shelter",
            organization_type=OrganizationType.NON_PROFIT,
            email="info@metroshelter.org",
            phone_number="512-555-0100",
            address_line1="500 Metro Blvd",
            city="Austin",
            state="TX",
            postal_code="78701",
            status=ShelterStatus.VERIFIED,
            is_active=True,
        )
        ShelterMember.objects.create(
            shelter=self.shelter,
            user=self.owner,
            role=ShelterMemberRole.OWNER,
            is_active=True,
        )
        self.verification = ShelterVerification.objects.create(
            shelter=self.shelter,
            status=VerificationStatus.APPROVED,
        )
        ShelterDocument.objects.create(
            shelter=self.shelter,
            verification=self.verification,
            document_type=DocumentType.GOVERNMENT_LICENSE,
            file_name="license.pdf",
            file_size=1024,
            status=DocumentStatus.APPROVED,
        )

    def test_get_shelter_dashboard_metrics_success(self):
        """Tests aggregating dashboard metrics for an active shelter."""
        metrics = DashboardService.get_shelter_dashboard_metrics(self.shelter.id)

        assert metrics["shelter_id"] == str(self.shelter.id)
        assert metrics["shelter_name"] == "Metro Animal Shelter"
        assert metrics["shelter_status"] == ShelterStatus.VERIFIED
        assert metrics["is_active"] is True
        assert metrics["is_verified"] is True
        assert metrics["can_publish_pets"] is True
        assert metrics["total_members"] == 1
        assert metrics["members_by_role"][ShelterMemberRole.OWNER] == 1
        assert metrics["total_documents"] == 1
        assert metrics["documents_by_status"][DocumentStatus.APPROVED] == 1
        assert metrics["verification_status"] == VerificationStatus.APPROVED

    def test_get_shelter_dashboard_metrics_not_found_raises_exception(self):
        """Tests that non-existent shelter ID raises ShelterNotFoundException."""
        random_id = uuid.uuid4()
        with pytest.raises(ShelterNotFoundException):
            DashboardService.get_shelter_dashboard_metrics(random_id)

    def test_get_system_dashboard_metrics_success(self):
        """Tests system-wide dashboard metrics aggregation for platform admin."""
        # Create second shelter
        Shelter.objects.create(
            name="Municipal Pound",
            slug="municipal-pound",
            organization_type=OrganizationType.MUNICIPAL,
            email="city@pound.gov",
            phone_number="512-555-0200",
            address_line1="100 City Hall",
            city="Austin",
            state="TX",
            postal_code="78701",
            status=ShelterStatus.UNVERIFIED,
            is_active=True,
        )

        sys_metrics = DashboardService.get_system_dashboard_metrics()

        assert sys_metrics["total_shelters"] == 2
        assert sys_metrics["active_shelters"] == 2
        assert sys_metrics["verified_shelters"] == 1
        assert sys_metrics["unverified_shelters"] == 1
        assert sys_metrics["shelters_by_type"][OrganizationType.NON_PROFIT] == 1
        assert sys_metrics["shelters_by_type"][OrganizationType.MUNICIPAL] == 1

"""
Service layer for Shelter dashboard metrics aggregation and reporting.
"""

import uuid
from typing import Any, Dict

from django.db.models import Count

from apps.shelters.constants import (
    DocumentStatus,
    InvitationStatus,
    ShelterMemberRole,
    ShelterStatus,
    VerificationStatus,
)
from apps.shelters.exceptions import ShelterNotFoundException
from apps.shelters.models import (
    Shelter,
    ShelterDocument,
    ShelterInvitation,
    ShelterMember,
    ShelterVerification,
)


class DashboardService:
    """Service handling dashboard data aggregation for shelters and system administrators."""

    @classmethod
    def get_shelter_dashboard(cls, shelter: Shelter) -> Dict[str, Any]:
        """
        Generates the standard shelter dashboard response dictionary.

        Response contract (Phase 2):
        - organization_name: Name of shelter organization.
        - verification_status: Verification / operational status string.
        - total_pets: Safe 0 default for Phase 2.
        - available_pets: Safe 0 default for Phase 2.
        - adopted_pets: Safe 0 default for Phase 2.
        - pending_applications: Safe 0 default for Phase 2.
        - recent_notifications: Empty list [] default for Phase 2.

        Extensible design allows plugging in Phase 3 Pets and Adoptions query logic seamlessly.
        """
        # Active verification state
        active_verification = (
            ShelterVerification.objects.filter(shelter=shelter)
            .order_by("-created_at")
            .first()
        )
        verification_status = (
            active_verification.status if active_verification else shelter.status
        )

        return {
            "organization_name": shelter.name,
            "verification_status": verification_status,
            "total_pets": 0,
            "available_pets": 0,
            "adopted_pets": 0,
            "pending_applications": 0,
            "recent_notifications": [],
            "is_verified": shelter.is_verified,
            "can_publish_pets": shelter.can_publish_pets,
        }

    @classmethod
    def get_shelter_dashboard_metrics(cls, shelter_id: uuid.UUID) -> Dict[str, Any]:
        """
        Aggregates detailed dashboard metrics and operational statistics for a specific shelter organization.

        Args:
            shelter_id: UUID of the shelter organization.

        Returns:
            Dict containing aggregated member counts, document statuses, invitation stats, and verification status.

        Raises:
            ShelterNotFoundException: If shelter does not exist or is soft-deleted.
        """
        try:
            shelter = Shelter.objects.get(id=shelter_id, is_deleted=False)
        except Shelter.DoesNotExist:
            raise ShelterNotFoundException(f"Shelter {shelter_id} not found.")

        # Member metrics
        members = ShelterMember.objects.filter(shelter=shelter, is_active=True)
        total_members = members.count()
        members_by_role = {
            role: members.filter(role=role).count() for role in ShelterMemberRole.values
        }

        # Document metrics
        documents = ShelterDocument.objects.filter(shelter=shelter)
        total_documents = documents.count()
        documents_by_status = {
            doc_status: documents.filter(status=doc_status).count()
            for doc_status in DocumentStatus.values
        }

        # Invitation metrics
        active_invitations = ShelterInvitation.objects.filter(
            shelter=shelter, status=InvitationStatus.PENDING
        ).count()

        # Active verification status
        active_verification = (
            ShelterVerification.objects.filter(shelter=shelter)
            .order_by("-created_at")
            .first()
        )
        verification_status = (
            active_verification.status
            if active_verification
            else VerificationStatus.DRAFT.value
        )

        dashboard_summary = cls.get_shelter_dashboard(shelter)
        dashboard_summary.update(
            {
                "shelter_id": str(shelter.id),
                "shelter_name": shelter.name,
                "shelter_status": shelter.status,
                "is_active": shelter.is_active,
                "total_members": total_members,
                "members_by_role": members_by_role,
                "total_documents": total_documents,
                "documents_by_status": documents_by_status,
                "active_invitations": active_invitations,
                "verification_status": verification_status,
            }
        )
        return dashboard_summary

    @classmethod
    def get_system_dashboard_metrics(cls) -> Dict[str, Any]:
        """
        Aggregates system-wide dashboard metrics across all shelter organizations for admin users.

        Returns:
            Dict containing platform-wide shelter counts, verification queue counts, and organization type breakdowns.
        """
        total_shelters = Shelter.objects.count()
        active_shelters = Shelter.objects.filter(is_active=True).count()
        verified_shelters = Shelter.objects.filter(
            status=ShelterStatus.VERIFIED
        ).count()
        unverified_shelters = Shelter.objects.filter(
            status=ShelterStatus.UNVERIFIED
        ).count()
        suspended_shelters = Shelter.objects.filter(
            status=ShelterStatus.SUSPENDED
        ).count()

        # Verification queue counts
        pending_verifications = ShelterVerification.objects.filter(
            status__in=[
                VerificationStatus.SUBMITTED,
                VerificationStatus.UNDER_REVIEW,
            ]
        ).count()

        # Shelters by organization type breakdown
        type_counts = (
            Shelter.objects.values("organization_type")
            .annotate(count=Count("id"))
            .order_by("organization_type")
        )
        shelters_by_type = {
            item["organization_type"]: item["count"] for item in type_counts
        }

        return {
            "total_shelters": total_shelters,
            "active_shelters": active_shelters,
            "verified_shelters": verified_shelters,
            "unverified_shelters": unverified_shelters,
            "suspended_shelters": suspended_shelters,
            "pending_verifications": pending_verifications,
            "shelters_by_type": shelters_by_type,
        }

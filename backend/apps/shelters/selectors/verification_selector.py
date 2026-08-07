"""
Selector layer for ShelterVerification workflow queries and document lookups.
"""

import uuid
from typing import Optional

from django.db.models import QuerySet

from apps.shelters.constants import VerificationStatus
from apps.shelters.models import ShelterDocument, ShelterVerification


def get_active_verification(shelter_id: uuid.UUID) -> Optional[ShelterVerification]:
    """Fetches the current active verification workflow for a shelter if one exists."""
    return (
        ShelterVerification.objects.select_related("shelter", "reviewed_by")
        .prefetch_related("documents")
        .filter(
            shelter_id=shelter_id,
            status__in=[
                VerificationStatus.DRAFT,
                VerificationStatus.SUBMITTED,
                VerificationStatus.UNDER_REVIEW,
                VerificationStatus.NEEDS_INFORMATION,
            ],
        )
        .first()
    )


def get_verification_by_id(
    verification_id: uuid.UUID,
) -> Optional[ShelterVerification]:
    """Fetches a verification workflow instance by ID with shelter and document optimization."""
    return (
        ShelterVerification.objects.select_related("shelter", "reviewed_by")
        .prefetch_related("documents")
        .filter(id=verification_id)
        .first()
    )


def list_shelter_documents(shelter_id: uuid.UUID) -> QuerySet[ShelterDocument]:
    """Lists all verification documents uploaded for a shelter."""
    return ShelterDocument.objects.filter(shelter_id=shelter_id).select_related(
        "uploaded_by", "verified_by"
    )

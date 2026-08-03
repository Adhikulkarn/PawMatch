"""
Selector layer for ShelterInvitation queries and token lookups.
"""

import uuid
from typing import Optional

from django.db.models import QuerySet

from apps.shelters.constants import InvitationStatus
from apps.shelters.models import ShelterInvitation


def get_invitation_by_token(token: str) -> Optional[ShelterInvitation]:
    """Fetches a shelter invitation by its unique token string."""
    return ShelterInvitation.objects.filter(token=token).first()


def get_pending_invitation_by_email(
    shelter_id: uuid.UUID, email: str
) -> Optional[ShelterInvitation]:
    """Fetches a pending invitation for a specific email and shelter if one exists."""
    return ShelterInvitation.objects.filter(
        shelter_id=shelter_id,
        email=email.strip().lower(),
        status=InvitationStatus.PENDING,
    ).first()


def list_shelter_invitations(shelter_id: uuid.UUID) -> QuerySet[ShelterInvitation]:
    """Lists all invitation records for a shelter."""
    return ShelterInvitation.objects.filter(shelter_id=shelter_id).select_related(
        "invited_by", "accepted_by"
    )

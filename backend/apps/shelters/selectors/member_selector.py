"""
Selector layer for ShelterMember queries and user membership lookups.
"""

import uuid
from typing import Optional

from django.db.models import QuerySet

from apps.shelters.constants import ShelterMemberRole
from apps.shelters.models import ShelterMember


def get_shelter_members(shelter_id: uuid.UUID) -> QuerySet[ShelterMember]:
    """Returns active member associations for a given shelter."""
    return ShelterMember.objects.filter(
        shelter_id=shelter_id, is_active=True
    ).select_related("user")


def get_user_shelter_membership(user_id: uuid.UUID) -> Optional[ShelterMember]:
    """Fetches the active shelter membership for a user if one exists."""
    return (
        ShelterMember.objects.select_related("shelter", "user")
        .filter(user_id=user_id, is_active=True)
        .first()
    )


def get_shelter_owners(shelter_id: uuid.UUID) -> QuerySet[ShelterMember]:
    """Returns active member associations with OWNER role for a shelter."""
    return ShelterMember.objects.filter(
        shelter_id=shelter_id, role=ShelterMemberRole.OWNER, is_active=True
    ).select_related("user")

"""
Selector layer for Shelter entity queries and public catalog filtering.
"""

import uuid
from typing import Optional

from django.db.models import QuerySet

from apps.shelters.constants import ShelterStatus
from apps.shelters.models import Shelter


def get_shelter_by_id(shelter_id: uuid.UUID) -> Optional[Shelter]:
    """Fetches an active, non-deleted shelter by ID."""
    return Shelter.objects.filter(id=shelter_id, is_deleted=False).first()


def get_shelter_by_slug(slug: str) -> Optional[Shelter]:
    """Fetches an active, non-deleted shelter by slug."""
    return Shelter.objects.filter(slug=slug, is_deleted=False).first()


def list_verified_shelters() -> QuerySet[Shelter]:
    """Returns a queryset of verified, active shelters available in the public catalog."""
    return Shelter.objects.filter(
        status=ShelterStatus.VERIFIED, is_active=True, is_deleted=False
    )

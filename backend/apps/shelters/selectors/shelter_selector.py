"""
Selector layer for Shelter entity queries and public catalog filtering.
"""

import uuid
from typing import Optional

from django.db.models import QuerySet

from apps.shelters.constants import ShelterStatus
from apps.shelters.models import Shelter


def get_shelter_by_id(shelter_id: uuid.UUID) -> Optional[Shelter]:
    """Fetches an active, non-deleted shelter by ID with address optimization."""
    return (
        Shelter.objects.select_related("address_rel")
        .filter(id=shelter_id, is_deleted=False)
        .first()
    )


def get_shelter_by_slug(slug: str) -> Optional[Shelter]:
    """Fetches an active, non-deleted shelter by slug with address optimization."""
    return (
        Shelter.objects.select_related("address_rel")
        .filter(slug=slug, is_deleted=False)
        .first()
    )


def list_verified_shelters() -> QuerySet[Shelter]:
    """Returns a queryset of verified, active shelters available in the public catalog."""
    return Shelter.objects.select_related("address_rel").filter(
        status=ShelterStatus.VERIFIED, is_active=True, is_deleted=False
    )


def list_all_shelters(
    status: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
) -> QuerySet[Shelter]:
    """
    Returns a filtered queryset of shelters with address pre-fetched.

    Args:
        status: Optional operational status filter.
        city: Optional city filter (case-insensitive).
        state: Optional state filter (case-insensitive).
    """
    qs = Shelter.objects.select_related("address_rel").filter(is_deleted=False)
    if status:
        qs = qs.filter(status=status)
    if city:
        qs = qs.filter(city__iexact=city)
    if state:
        qs = qs.filter(state__iexact=state)
    return qs


def get_shelters_by_status(status: str) -> QuerySet[Shelter]:
    """Returns all non-deleted shelters matching a given status with pre-fetched address."""
    return Shelter.objects.select_related("address_rel").filter(
        status=status, is_deleted=False
    )


def search_shelters(query: str) -> QuerySet[Shelter]:
    """Searches active, non-deleted shelters by name, legal name, city, or state."""
    return (
        Shelter.objects.select_related("address_rel")
        .search(query)
        .filter(is_deleted=False)
    )

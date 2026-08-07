"""
Custom QuerySets and Managers for Shelter domain models.
"""

from typing import Self

from django.db import models

from apps.shelters.constants import DocumentStatus, ShelterStatus


class ShelterQuerySet(models.QuerySet):
    """Custom QuerySet for Shelter model operations."""

    def active(self) -> Self:
        """Filter for active, non-deleted shelters."""
        return self.filter(is_active=True, is_deleted=False)

    def verified(self) -> Self:
        """Filter for verified shelters."""
        return self.filter(status=ShelterStatus.VERIFIED, is_deleted=False)

    def unverified(self) -> Self:
        """Filter for unverified shelters."""
        return self.filter(status=ShelterStatus.UNVERIFIED, is_deleted=False)

    def by_city(self, city: str) -> Self:
        """Filter shelters by city (case-insensitive)."""
        return self.filter(city__iexact=city)

    def by_state(self, state: str) -> Self:
        """Filter shelters by state (case-insensitive)."""
        return self.filter(state__iexact=state)

    def search(self, query: str) -> Self:
        """Search shelters by name, legal name, city, or state."""
        if not query:
            return self
        return self.filter(
            models.Q(name__icontains=query)
            | models.Q(legal_name__icontains=query)
            | models.Q(city__icontains=query)
            | models.Q(state__icontains=query)
        )


class ShelterManager(models.Manager.from_queryset(ShelterQuerySet)):
    """Custom Manager for Shelter model using ShelterQuerySet."""

    def get_queryset(self) -> ShelterQuerySet:
        """Returns default queryset excluding soft-deleted records."""
        return ShelterQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def with_deleted(self) -> ShelterQuerySet:
        """Returns queryset including soft-deleted records."""
        return ShelterQuerySet(self.model, using=self._db)


class ShelterAddressQuerySet(models.QuerySet):
    """Custom QuerySet for ShelterAddress model operations."""

    def by_city(self, city: str) -> Self:
        """Filter shelter addresses by city (case-insensitive)."""
        return self.filter(city__iexact=city)

    def by_state(self, state: str) -> Self:
        """Filter shelter addresses by state (case-insensitive)."""
        return self.filter(state__iexact=state)

    def with_coordinates(self) -> Self:
        """Filter addresses that have latitude and longitude set."""
        return self.filter(latitude__isnull=False, longitude__isnull=False)


class ShelterAddressManager(models.Manager.from_queryset(ShelterAddressQuerySet)):
    """Custom Manager for ShelterAddress model using ShelterAddressQuerySet."""

    pass


class ShelterDocumentQuerySet(models.QuerySet):
    """Custom QuerySet for ShelterDocument model operations."""

    def approved(self) -> Self:
        """Filter for approved documents."""
        return self.filter(status=DocumentStatus.APPROVED)

    def pending(self) -> Self:
        """Filter for pending verification documents."""
        return self.filter(status=DocumentStatus.PENDING)

    def rejected(self) -> Self:
        """Filter for rejected verification documents."""
        return self.filter(status=DocumentStatus.REJECTED)

    def by_type(self, doc_type: str) -> Self:
        """Filter documents by document type."""
        return self.filter(document_type=doc_type)


class ShelterDocumentManager(models.Manager.from_queryset(ShelterDocumentQuerySet)):
    """Custom Manager for ShelterDocument model using ShelterDocumentQuerySet."""

    pass

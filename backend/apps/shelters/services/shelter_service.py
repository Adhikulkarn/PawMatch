"""
Service layer for Shelter organization lifecycle management and onboarding.
"""

import uuid
from typing import Any, Dict, Optional

from django.db import transaction
from django.utils.text import slugify

from apps.shelters.constants import (
    ShelterMemberRole,
    ShelterStatus,
    VerificationStatus,
)
from apps.shelters.exceptions import (
    MemberAlreadyExistsException,
    ShelterNotFoundException,
)
from apps.shelters.models import Shelter, ShelterMember, ShelterVerification


class ShelterService:
    """Service handling shelter organization creation, updates, and lifecycle transitions."""

    @staticmethod
    def generate_unique_slug(name: str) -> str:
        """Generates a URL-friendly, unique slug for a shelter based on its name."""
        base_slug = slugify(name) or "shelter"
        slug = base_slug
        counter = 1

        while Shelter.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    @classmethod
    def create_shelter(
        cls,
        user: Any,
        name: str,
        email: str,
        phone_number: str,
        address_line1: str,
        city: str,
        state: str,
        postal_code: str,
        country: str = "USA",
        legal_name: str = "",
        registration_number: str = "",
        tax_id: str = "",
        address_line2: str = "",
        website: str = "",
        description: str = "",
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        logo: Any = None,
        banner_image: Any = None,
    ) -> Shelter:
        """
        Onboards a new Shelter organization.

        Business Rules:
        - BR-201: Shelter starts in UNVERIFIED status.
        - BR-203: Owner membership record created for user.
        - BR-204: User cannot belong to multiple active shelters.
        - Initial draft verification workflow is initialized.
        """
        # BR-204 Check: Ensure user does not already belong to a shelter
        if ShelterMember.objects.filter(user=user, is_active=True).exists():
            raise MemberAlreadyExistsException(
                f"User {user.email} already belongs to an active shelter."
            )

        slug = cls.generate_unique_slug(name)

        with transaction.atomic():
            shelter = Shelter.objects.create(
                name=name,
                slug=slug,
                legal_name=legal_name,
                registration_number=registration_number,
                tax_id=tax_id,
                email=email,
                phone_number=phone_number,
                website=website,
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                latitude=latitude,
                longitude=longitude,
                description=description,
                logo=logo,
                banner_image=banner_image,
                status=ShelterStatus.UNVERIFIED,
                is_active=True,
            )

            # BR-203: Create owner membership
            ShelterMember.objects.create(
                shelter=shelter,
                user=user,
                role=ShelterMemberRole.OWNER,
                is_active=True,
            )

            # Initialize initial draft verification workflow
            ShelterVerification.objects.create(
                shelter=shelter,
                status=VerificationStatus.DRAFT,
            )

        return shelter

    @classmethod
    def update_shelter(cls, shelter_id: uuid.UUID, **kwargs: Dict[str, Any]) -> Shelter:
        """Updates shelter profile attributes."""
        try:
            shelter = Shelter.objects.get(id=shelter_id, is_deleted=False)
        except Shelter.DoesNotExist:
            raise ShelterNotFoundException(f"Shelter {shelter_id} not found.")

        # If name is being updated, regenerate unique slug
        if "name" in kwargs and kwargs["name"] != shelter.name:
            shelter.slug = cls.generate_unique_slug(kwargs["name"])

        for field, value in kwargs.items():
            if hasattr(shelter, field) and field not in [
                "id",
                "created_at",
                "updated_at",
            ]:
                setattr(shelter, field, value)

        shelter.save()
        return shelter

    @classmethod
    def archive_shelter(cls, shelter_id: uuid.UUID) -> Shelter:
        """Archives a shelter organization and deactivates platform presence."""
        try:
            shelter = Shelter.objects.get(id=shelter_id, is_deleted=False)
        except Shelter.DoesNotExist:
            raise ShelterNotFoundException(f"Shelter {shelter_id} not found.")

        shelter.status = ShelterStatus.ARCHIVED
        shelter.is_active = False
        shelter.save(update_fields=["status", "is_active", "updated_at"])
        return shelter

    @classmethod
    def suspend_shelter(cls, shelter_id: uuid.UUID) -> Shelter:
        """Suspends a shelter organization due to administrative action."""
        try:
            shelter = Shelter.objects.get(id=shelter_id, is_deleted=False)
        except Shelter.DoesNotExist:
            raise ShelterNotFoundException(f"Shelter {shelter_id} not found.")

        shelter.status = ShelterStatus.SUSPENDED
        shelter.is_active = False
        shelter.save(update_fields=["status", "is_active", "updated_at"])
        return shelter

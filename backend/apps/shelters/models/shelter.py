"""
Shelter entity definition representing an organization.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.mixins import SoftDeleteModel, TimestampedModel, UUIDModel
from apps.shelters.constants import ShelterMemberRole, ShelterStatus


class Shelter(UUIDModel, TimestampedModel, SoftDeleteModel):
    """
    Represents a pet shelter organization.
    Stores public profile, contact information, legal details, and operational status.

    Ownership Rule (BR-203):
    Ownership is NOT stored via a direct ForeignKey on Shelter.
    Instead, ownership is determined by membership records in ShelterMember with role OWNER.
    """

    name = models.CharField(_("shelter name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, db_index=True)
    legal_name = models.CharField(
        _("legal name"), max_length=255, blank=True, default=""
    )
    registration_number = models.CharField(
        _("registration number"), max_length=100, blank=True, default=""
    )
    tax_id = models.CharField(_("tax ID"), max_length=100, blank=True, default="")

    email = models.EmailField(_("shelter email"), db_index=True)
    phone_number = models.CharField(_("phone number"), max_length=30)
    website = models.URLField(_("website URL"), blank=True, default="")

    address_line1 = models.CharField(_("address line 1"), max_length=255)
    address_line2 = models.CharField(
        _("address line 2"), max_length=255, blank=True, default=""
    )
    city = models.CharField(_("city"), max_length=100, db_index=True)
    state = models.CharField(_("state / province"), max_length=100, db_index=True)
    postal_code = models.CharField(_("postal code"), max_length=20)
    country = models.CharField(_("country"), max_length=100, default="USA")

    latitude = models.DecimalField(
        _("latitude"), max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        _("longitude"), max_digits=9, decimal_places=6, null=True, blank=True
    )

    description = models.TextField(_("description"), blank=True, default="")
    logo = models.ImageField(
        _("logo image"), upload_to="shelters/logos/", null=True, blank=True
    )
    banner_image = models.ImageField(
        _("banner image"), upload_to="shelters/banners/", null=True, blank=True
    )

    status = models.CharField(
        _("shelter status"),
        max_length=30,
        choices=ShelterStatus.choices,
        default=ShelterStatus.UNVERIFIED,
        db_index=True,
    )
    is_active = models.BooleanField(
        _("active status"),
        default=True,
        db_index=True,
        help_text=_("Designates whether this shelter is active on the platform."),
    )

    class Meta:
        verbose_name = _("shelter")
        verbose_name_plural = _("shelters")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["city", "state"]),
            models.Index(fields=["status", "is_active"]),
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def is_verified(self) -> bool:
        """Returns True if the shelter has achieved VERIFIED status."""
        return self.status == ShelterStatus.VERIFIED

    @property
    def can_publish_pets(self) -> bool:
        """
        Business Rule BR-202:
        Only verified, active, non-deleted shelters may publish pet listings.
        """
        return self.is_verified and self.is_active and not self.is_deleted

    @property
    def owner_memberships(self):
        """Returns queryset of ShelterMember records with OWNER role for this shelter."""
        return self.members.filter(
            role=ShelterMemberRole.OWNER, is_active=True
        )

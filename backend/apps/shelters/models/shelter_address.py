"""
ShelterAddress entity definition representing structured geographic location of a shelter.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.mixins import TimestampedModel, UUIDModel
from apps.shelters.managers import ShelterAddressManager


class ShelterAddress(UUIDModel, TimestampedModel):
    """
    Represents the physical location and geographic coordinates of a Shelter organization.
    """

    shelter = models.OneToOneField(
        "shelters.Shelter",
        on_delete=models.CASCADE,
        related_name="address_rel",
        verbose_name=_("shelter"),
    )
    address_line1 = models.CharField(_("address line 1"), max_length=255)
    address_line2 = models.CharField(
        _("address line 2"), max_length=255, blank=True, default=""
    )
    city = models.CharField(_("city"), max_length=100, db_index=True)
    state = models.CharField(_("state / province"), max_length=100, db_index=True)
    postal_code = models.CharField(_("postal code"), max_length=20, db_index=True)
    country = models.CharField(_("country"), max_length=100, default="USA")

    latitude = models.DecimalField(
        _("latitude"), max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        _("longitude"), max_digits=9, decimal_places=6, null=True, blank=True
    )
    is_primary = models.BooleanField(_("is primary address"), default=True)

    objects = ShelterAddressManager()

    class Meta:
        verbose_name = _("shelter address")
        verbose_name_plural = _("shelter addresses")
        ordering = ["city", "state"]
        indexes = [
            models.Index(fields=["city", "state"]),
            models.Index(fields=["postal_code"]),
        ]

    def __str__(self) -> str:
        return self.formatted_address

    @property
    def formatted_address(self) -> str:
        """Returns single-line formatted address string."""
        line2 = f", {self.address_line2}" if self.address_line2 else ""
        return f"{self.address_line1}{line2}, {self.city}, {self.state} {self.postal_code}, {self.country}"

    @property
    def has_coordinates(self) -> bool:
        """Returns True if latitude and longitude are both populated."""
        return self.latitude is not None and self.longitude is not None

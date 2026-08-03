"""
ShelterMember entity definition representing a User's membership inside a Shelter.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.mixins import TimestampedModel, UUIDModel
from apps.shelters.constants import ShelterMemberRole


class ShelterMember(UUIDModel, TimestampedModel):
    """
    Represents the membership relationship of a User within a Shelter organization.

    Business Rules:
    - BR-203: A shelter must always have at least one OWNER.
    - BR-204: Enforce single active shelter membership via UniqueConstraint(user, shelter).
    """

    # CASCADE: Shelter deletion invalidates and removes all member associations.
    shelter = models.ForeignKey(
        "shelters.Shelter",
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name=_("shelter"),
    )
    # CASCADE: Deleting a user account removes their membership record.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shelter_memberships",
        verbose_name=_("user"),
        help_text=_("The user account associated with this shelter membership."),
    )
    role = models.CharField(
        _("membership role"),
        max_length=30,
        choices=ShelterMemberRole.choices,
        default=ShelterMemberRole.VOLUNTEER,
        db_index=True,
    )
    is_active = models.BooleanField(
        _("active status"),
        default=True,
        db_index=True,
        help_text=_("Designates whether this user membership is currently active."),
    )
    joined_at = models.DateTimeField(_("joined at"), auto_now_add=True)

    class Meta:
        verbose_name = _("shelter member")
        verbose_name_plural = _("shelter members")
        ordering = ["-joined_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "shelter"],
                name="unique_shelter_user_membership",
            ),
        ]
        indexes = [
            models.Index(fields=["shelter", "role"]),
            models.Index(fields=["shelter", "is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.shelter.name} ({self.get_role_display()})"

    @property
    def is_owner(self) -> bool:
        """Returns True if member has OWNER role."""
        return self.role == ShelterMemberRole.OWNER

    @property
    def is_manager(self) -> bool:
        """Returns True if member has OWNER or MANAGER role."""
        return self.role in [ShelterMemberRole.OWNER, ShelterMemberRole.MANAGER]

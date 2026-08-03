"""
ShelterInvitation entity definition representing staff/volunteer membership invitations.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.mixins import TimestampedModel, UUIDModel
from apps.shelters.constants import InvitationStatus, ShelterMemberRole


class ShelterInvitation(UUIDModel, TimestampedModel):
    """
    Represents a pending invitation sent to a user's email to join a shelter organization.

    Business Rules:
    - BR-205: Invitations expire after a configurable duration (expires_at).
    """

    # CASCADE: Invitations to join a shelter are invalid if the shelter organization itself is deleted.
    shelter = models.ForeignKey(
        "shelters.Shelter",
        on_delete=models.CASCADE,
        related_name="invitations",
        verbose_name=_("shelter"),
    )
    email = models.EmailField(_("invited email"), db_index=True)
    role = models.CharField(
        _("invited role"),
        max_length=30,
        choices=ShelterMemberRole.choices,
        default=ShelterMemberRole.VOLUNTEER,
    )
    token = models.CharField(
        _("invitation token"), max_length=100, unique=True, db_index=True
    )
    status = models.CharField(
        _("invitation status"),
        max_length=30,
        choices=InvitationStatus.choices,
        default=InvitationStatus.PENDING,
        db_index=True,
    )
    # SET_NULL: Retains invitation record and history even if inviting manager account is removed.
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_shelter_invitations",
        verbose_name=_("invited by user"),
    )
    # SET_NULL: Retains invitation acceptance history even if accepting user account is removed.
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_shelter_invitations",
        verbose_name=_("accepted by user"),
    )
    accepted_at = models.DateTimeField(_("accepted at"), null=True, blank=True)
    expires_at = models.DateTimeField(_("expires at"), db_index=True)
    responded_at = models.DateTimeField(_("responded at"), null=True, blank=True)

    class Meta:
        verbose_name = _("shelter invitation")
        verbose_name_plural = _("shelter invitations")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["shelter", "email"],
                condition=models.Q(status=InvitationStatus.PENDING),
                name="unique_pending_shelter_invitation",
            ),
        ]
        indexes = [
            models.Index(fields=["token", "status"]),
            models.Index(fields=["shelter", "status"]),
        ]

    def __str__(self) -> str:
        return f"Invitation for {self.email} to join {self.shelter.name} as {self.get_role_display()}"

    @property
    def is_expired(self) -> bool:
        """Business Rule BR-205: Returns True if current time has passed expires_at timestamp."""
        return timezone.now() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Returns True if the invitation is PENDING and has not expired."""
        return self.status == InvitationStatus.PENDING and not self.is_expired

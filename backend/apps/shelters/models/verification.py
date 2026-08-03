"""
ShelterVerification entity definition representing the verification workflow state.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.mixins import TimestampedModel, UUIDModel
from apps.shelters.constants import VerificationStatus


class ShelterVerification(UUIDModel, TimestampedModel):
    """
    Represents a verification request lifecycle for a shelter organization.

    State Machine Transitions:
    Draft -> Submitted -> Under Review -> Approved
    Alternative paths:
    Under Review -> Needs Information -> Submitted
    Under Review -> Rejected

    Business Rules:
    - BR-201: Shelters may exist before verification.
    - BR-206: Rejected verification requires new submission.
    """

    # CASCADE: Verification requests belong exclusively to a shelter; deleting shelter removes workflows.
    shelter = models.ForeignKey(
        "shelters.Shelter",
        on_delete=models.CASCADE,
        related_name="verifications",
        verbose_name=_("shelter"),
    )
    status = models.CharField(
        _("verification status"),
        max_length=30,
        choices=VerificationStatus.choices,
        default=VerificationStatus.DRAFT,
        db_index=True,
    )
    # SET_NULL: Preserves verification decision history even if reviewing staff account is deleted.
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_verifications",
        verbose_name=_("reviewed by staff user"),
    )
    reviewer_notes = models.TextField(
        _("reviewer notes"),
        blank=True,
        default="",
        help_text=_("Internal staff notes and observations regarding verification."),
    )
    rejection_reason = models.TextField(
        _("rejection reason"),
        blank=True,
        default="",
        help_text=_(
            "Feedback provided to shelter if verification is rejected or needs information."
        ),
    )
    submitted_at = models.DateTimeField(_("submitted at"), null=True, blank=True)
    reviewed_at = models.DateTimeField(_("reviewed at"), null=True, blank=True)

    class Meta:
        verbose_name = _("shelter verification")
        verbose_name_plural = _("shelter verifications")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["shelter"],
                condition=models.Q(
                    status__in=[
                        VerificationStatus.DRAFT,
                        VerificationStatus.SUBMITTED,
                        VerificationStatus.UNDER_REVIEW,
                        VerificationStatus.NEEDS_INFORMATION,
                    ]
                ),
                name="unique_active_shelter_verification",
            ),
        ]
        indexes = [
            models.Index(fields=["shelter", "status"]),
            models.Index(fields=["status", "submitted_at"]),
        ]

    def __str__(self) -> str:
        return f"Verification for {self.shelter.name} ({self.get_status_display()})"

    @property
    def is_active_workflow(self) -> bool:
        """Returns True if the verification is in a non-terminal active workflow state."""
        return self.status in [
            VerificationStatus.DRAFT,
            VerificationStatus.SUBMITTED,
            VerificationStatus.UNDER_REVIEW,
            VerificationStatus.NEEDS_INFORMATION,
        ]

    @property
    def is_approved(self) -> bool:
        """Returns True if the verification has been approved."""
        return self.status == VerificationStatus.APPROVED

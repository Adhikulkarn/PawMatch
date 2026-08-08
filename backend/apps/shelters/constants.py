"""
Constants and TextChoices for the Shelter domain.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ShelterStatus(models.TextChoices):
    """Operational lifecycle status of a Shelter entity."""

    UNVERIFIED = "unverified", _("Unverified")
    VERIFIED = "verified", _("Verified")
    SUSPENDED = "suspended", _("Suspended")
    ARCHIVED = "archived", _("Archived")


class OrganizationType(models.TextChoices):
    """Legal organization type of a shelter entity."""

    NON_PROFIT = "non_profit", _("Non-Profit / NGO")
    MUNICIPAL = "municipal", _("Municipal / Government Shelter")
    PRIVATE = "private", _("Private Rescue / Sanctuary")
    FOSTER_NETWORK = "foster_network", _("Foster Network")
    OTHER = "other", _("Other")


class VerificationStatus(models.TextChoices):
    """Workflow state machine statuses for ShelterVerification requests."""

    DRAFT = "draft", _("Draft")
    SUBMITTED = "submitted", _("Submitted")
    UNDER_REVIEW = "under_review", _("Under Review")
    NEEDS_INFORMATION = "needs_information", _("Needs Information")
    APPROVED = "approved", _("Approved")
    REJECTED = "rejected", _("Rejected")


class ShelterMemberRole(models.TextChoices):
    """Membership roles for users within a shelter organization."""

    OWNER = "owner", _("Owner")
    MANAGER = "manager", _("Manager")
    STAFF = "staff", _("Staff")
    VOLUNTEER = "volunteer", _("Volunteer")
    VETERINARIAN = "veterinarian", _("Veterinarian")
    VIEWER = "viewer", _("Viewer")


class DocumentType(models.TextChoices):
    """Types of legal and verification documents required for shelter verification."""

    REGISTRATION_CERTIFICATE = (
        "registration_certificate",
        _("Registration Certificate"),
    )
    NGO_CERTIFICATE = "ngo_certificate", _("NGO Certificate")
    GOVERNMENT_LICENSE = "government_license", _("Government License")
    ADDRESS_PROOF = "address_proof", _("Address Proof")
    IDENTITY_PROOF = "identity_proof", _("Identity Proof")
    TAX_CERTIFICATE = "tax_certificate", _("Tax Certificate")
    OTHER = "other", _("Other")


class DocumentStatus(models.TextChoices):
    """Status of an uploaded verification document."""

    PENDING = "pending", _("Pending Review")
    APPROVED = "approved", _("Approved")
    REJECTED = "rejected", _("Rejected")


class InvitationStatus(models.TextChoices):
    """Lifecycle statuses for shelter staff/volunteer invitations."""

    PENDING = "pending", _("Pending")
    ACCEPTED = "accepted", _("Accepted")
    DECLINED = "declined", _("Declined")
    EXPIRED = "expired", _("Expired")
    REVOKED = "revoked", _("Revoked")


# Default expiration time for shelter member invitations (in days)
DEFAULT_INVITATION_EXPIRY_DAYS = 7

"""
Shared domain choice enums across PawMatch applications.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    """User account access roles."""

    ADOPTER = "ADOPTER", _("Adopter")
    SHELTER_ADMIN = "SHELTER_ADMIN", _("Shelter Admin")
    SHELTER_STAFF = "SHELTER_STAFF", _("Shelter Staff")
    SYSTEM_ADMIN = "SYSTEM_ADMIN", _("System Admin")


class PetSpecies(models.TextChoices):
    """Supported pet species."""

    DOG = "DOG", _("Dog")
    CAT = "CAT", _("Cat")
    BIRD = "BIRD", _("Bird")
    RABBIT = "RABBIT", _("Rabbit")
    OTHER = "OTHER", _("Other")


class PetStatus(models.TextChoices):
    """Pet adoption availability status."""

    AVAILABLE = "AVAILABLE", _("Available")
    PENDING = "PENDING", _("Pending Adoption")
    ADOPTED = "ADOPTED", _("Adopted")
    FOSTERED = "FOSTERED", _("Fostered")
    UNAVAILABLE = "UNAVAILABLE", _("Unavailable")


class ApplicationStatus(models.TextChoices):
    """Adoption application workflow status."""

    SUBMITTED = "SUBMITTED", _("Submitted")
    UNDER_REVIEW = "UNDER_REVIEW", _("Under Review")
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED", _("Interview Scheduled")
    APPROVED = "APPROVED", _("Approved")
    REJECTED = "REJECTED", _("Rejected")
    WITHDRAWN = "WITHDRAWN", _("Withdrawn")

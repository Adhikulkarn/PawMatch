"""
Custom domain exceptions for the Shelter bounded context.
"""


class ShelterDomainException(Exception):
    """Base exception for all Shelter domain errors."""

    pass


class ShelterNotFoundException(ShelterDomainException):
    """Raised when a requested shelter does not exist or is soft-deleted."""

    pass


class VerificationWorkflowException(ShelterDomainException):
    """Raised when an invalid state transition is attempted on ShelterVerification."""

    pass


class MemberAlreadyExistsException(ShelterDomainException):
    """Raised when a user is already assigned to a shelter (BR-204)."""

    pass


class LastOwnerRemovalException(ShelterDomainException):
    """Raised when attempting to remove or downgrade the last OWNER of a shelter (BR-203)."""

    pass


class InvitationExpiredException(ShelterDomainException):
    """Raised when attempting to accept an expired or invalid invitation (BR-205)."""

    pass


class DocumentProtectedException(ShelterDomainException):
    """Raised when attempting to delete or modify an approved verification document (BR-207)."""

    pass


class UnverifiedShelterActionException(ShelterDomainException):
    """Raised when an unverified shelter attempts an operation requiring verification (BR-202)."""

    pass

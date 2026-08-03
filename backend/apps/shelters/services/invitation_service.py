"""
Service layer for Shelter staff/volunteer invitation management.
"""

import secrets
import uuid
from datetime import timedelta
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.shelters.constants import (
    DEFAULT_INVITATION_EXPIRY_DAYS,
    InvitationStatus,
    ShelterMemberRole,
)
from apps.shelters.exceptions import (
    InvitationExpiredException,
    MemberAlreadyExistsException,
    ShelterDomainException,
)
from apps.shelters.models import Shelter, ShelterInvitation, ShelterMember


class InvitationService:
    """Service handling tokenized shelter invitations and acceptance workflows."""

    @classmethod
    def create_invitation(
        cls,
        shelter: Shelter,
        email: str,
        role: str = ShelterMemberRole.VOLUNTEER,
        invited_by: Any = None,
        expiry_days: int = DEFAULT_INVITATION_EXPIRY_DAYS,
    ) -> ShelterInvitation:
        """
        Creates and dispatches a tokenized invitation to an email.

        Business Rules:
        - Prevents duplicate pending invitations for same (shelter, email).
        - BR-205: Sets expiration timestamp.
        """
        email_clean = email.strip().lower()

        # Ensure email is not already an active member of this shelter
        if ShelterMember.objects.filter(
            shelter=shelter, user__email=email_clean, is_active=True
        ).exists():
            raise MemberAlreadyExistsException(
                f"User with email {email_clean} is already a member of {shelter.name}."
            )

        # Check for existing pending invitation
        if ShelterInvitation.objects.filter(
            shelter=shelter, email=email_clean, status=InvitationStatus.PENDING
        ).exists():
            raise ShelterDomainException(
                f"A pending invitation already exists for {email_clean}."
            )

        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(days=expiry_days)

        invitation = ShelterInvitation.objects.create(
            shelter=shelter,
            email=email_clean,
            role=role,
            token=token,
            status=InvitationStatus.PENDING,
            invited_by=invited_by,
            expires_at=expires_at,
        )
        return invitation

    @classmethod
    def accept_invitation(cls, token: str, user: Any) -> ShelterMember:
        """
        Accepts a valid shelter invitation and creates user membership.

        Business Rules:
        - BR-204: Ensures user does not already belong to an active shelter.
        - BR-205: Rejects expired invitations.
        """
        try:
            invitation = ShelterInvitation.objects.get(token=token)
        except ShelterInvitation.DoesNotExist:
            raise ShelterDomainException("Invalid or non-existent invitation token.")

        if invitation.status != InvitationStatus.PENDING:
            raise ShelterDomainException(
                f"Invitation is no longer pending (current status: {invitation.status})."
            )

        if invitation.is_expired:
            invitation.status = InvitationStatus.EXPIRED
            invitation.save(update_fields=["status", "updated_at"])
            raise InvitationExpiredException("Invitation has expired (BR-205).")

        # BR-204 Check: Ensure user does not already belong to another active shelter
        if ShelterMember.objects.filter(user=user, is_active=True).exists():
            raise MemberAlreadyExistsException(
                f"User {user.email} already belongs to an active shelter (BR-204)."
            )

        with transaction.atomic():
            member = ShelterMember.objects.create(
                shelter=invitation.shelter,
                user=user,
                role=invitation.role,
                is_active=True,
            )

            invitation.status = InvitationStatus.ACCEPTED
            invitation.accepted_by = user
            invitation.accepted_at = timezone.now()
            invitation.responded_at = timezone.now()
            invitation.save()

        return member

    @classmethod
    def expire_invitation(cls, invitation_id: uuid.UUID) -> ShelterInvitation:
        """Marks an invitation as expired."""
        try:
            invitation = ShelterInvitation.objects.get(id=invitation_id)
        except ShelterInvitation.DoesNotExist:
            raise ShelterDomainException("Invitation not found.")

        invitation.status = InvitationStatus.EXPIRED
        invitation.save(update_fields=["status", "updated_at"])
        return invitation

    @classmethod
    def revoke_invitation(cls, invitation_id: uuid.UUID) -> ShelterInvitation:
        """Revokes a pending shelter invitation."""
        try:
            invitation = ShelterInvitation.objects.get(id=invitation_id)
        except ShelterInvitation.DoesNotExist:
            raise ShelterDomainException("Invitation not found.")

        invitation.status = InvitationStatus.REVOKED
        invitation.responded_at = timezone.now()
        invitation.save(update_fields=["status", "responded_at", "updated_at"])
        return invitation

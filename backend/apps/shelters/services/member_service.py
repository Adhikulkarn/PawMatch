"""
Service layer for Shelter membership management, role changes, and ownership transfers.
"""

import uuid
from typing import Any, Tuple

from django.db import transaction

from apps.shelters.constants import ShelterMemberRole
from apps.shelters.exceptions import (
    LastOwnerRemovalException,
    MemberAlreadyExistsException,
    ShelterDomainException,
)
from apps.shelters.models import Shelter, ShelterMember


class MemberService:
    """Service handling shelter member management and ownership safeguards."""

    @classmethod
    def add_member(
        cls,
        shelter: Shelter,
        user: Any,
        role: str = ShelterMemberRole.VOLUNTEER,
    ) -> ShelterMember:
        """
        Adds a user as a member of a shelter organization.

        Business Rules:
        - BR-204: Ensures user does not already belong to an active shelter.
        """
        if ShelterMember.objects.filter(user=user, is_active=True).exists():
            raise MemberAlreadyExistsException(
                f"User {user.email} already belongs to an active shelter (BR-204)."
            )

        member = ShelterMember.objects.create(
            shelter=shelter,
            user=user,
            role=role,
            is_active=True,
        )
        return member

    @classmethod
    def remove_member(cls, shelter_member_id: uuid.UUID) -> None:
        """
        Removes a member from a shelter organization.

        Business Rules:
        - BR-203: A shelter must always have at least one OWNER.
                  Prevents removing the last remaining OWNER of a shelter.
        - Uses atomic transaction and row-level locking to prevent race conditions.
        """
        with transaction.atomic():
            try:
                member = ShelterMember.objects.select_for_update().get(
                    id=shelter_member_id
                )
            except ShelterMember.DoesNotExist:
                raise ShelterDomainException("Shelter member not found.")

            if member.role == ShelterMemberRole.OWNER and member.is_active:
                active_owners_count = (
                    ShelterMember.objects.select_for_update()
                    .filter(
                        shelter=member.shelter,
                        role=ShelterMemberRole.OWNER,
                        is_active=True,
                    )
                    .count()
                )
                if active_owners_count <= 1:
                    raise LastOwnerRemovalException(
                        "Cannot remove the last remaining OWNER of a shelter (BR-203)."
                    )

            member.delete()

    @classmethod
    def change_role(cls, shelter_member_id: uuid.UUID, new_role: str) -> ShelterMember:
        """
        Updates the membership role of a shelter user.

        Business Rules:
        - BR-203: Prevents downgrading the last remaining OWNER of a shelter.
        - Uses atomic transaction and row-level locking to prevent race conditions.
        """
        with transaction.atomic():
            try:
                member = ShelterMember.objects.select_for_update().get(
                    id=shelter_member_id
                )
            except ShelterMember.DoesNotExist:
                raise ShelterDomainException("Shelter member not found.")

            if (
                member.role == ShelterMemberRole.OWNER
                and new_role != ShelterMemberRole.OWNER
                and member.is_active
            ):
                active_owners_count = (
                    ShelterMember.objects.select_for_update()
                    .filter(
                        shelter=member.shelter,
                        role=ShelterMemberRole.OWNER,
                        is_active=True,
                    )
                    .count()
                )
                if active_owners_count <= 1:
                    raise LastOwnerRemovalException(
                        "Cannot demote the last remaining OWNER of a shelter (BR-203)."
                    )

            member.role = new_role
            member.save(update_fields=["role", "updated_at"])
            return member

    @classmethod
    def transfer_ownership(
        cls, shelter: Shelter, current_owner_user: Any, new_owner_user: Any
    ) -> Tuple[ShelterMember, ShelterMember]:
        """
        Transfers primary ownership of a shelter from current owner to a new owner user.

        Business Rules:
        - BR-203: Guarantees at least one active OWNER at all times.
        - Wrapped in an atomic transaction to prevent orphaned states.
        """
        try:
            current_owner_member = ShelterMember.objects.get(
                shelter=shelter,
                user=current_owner_user,
                role=ShelterMemberRole.OWNER,
                is_active=True,
            )
        except ShelterMember.DoesNotExist:
            raise ShelterDomainException(
                f"User {current_owner_user.email} is not an active OWNER of {shelter.name}."
            )

        with transaction.atomic():
            # Promote new owner user to OWNER role
            new_owner_member, created = ShelterMember.objects.get_or_create(
                shelter=shelter,
                user=new_owner_user,
                defaults={"role": ShelterMemberRole.OWNER, "is_active": True},
            )
            if not created:
                new_owner_member.role = ShelterMemberRole.OWNER
                new_owner_member.is_active = True
                new_owner_member.save(update_fields=["role", "is_active", "updated_at"])

            # Demote former owner to MANAGER role
            current_owner_member.role = ShelterMemberRole.MANAGER
            current_owner_member.save(update_fields=["role", "updated_at"])

        return current_owner_member, new_owner_member

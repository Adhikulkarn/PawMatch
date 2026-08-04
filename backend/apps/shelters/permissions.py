"""
Permission classes for Shelter domain access control and object-level authorization.
Integrates with PawMatch RBAC and Accounts authorization framework.
"""

import uuid
from typing import Any, Optional

from rest_framework.permissions import BasePermission

from apps.accounts.roles import RoleName
from apps.shelters.constants import ShelterMemberRole, ShelterStatus
from apps.shelters.models import (
    Shelter,
    ShelterDocument,
    ShelterInvitation,
    ShelterMember,
)


def _to_uuid(val: Any) -> Optional[uuid.UUID]:
    """Helper converting string or UUID instance cleanly to a uuid.UUID object."""
    if isinstance(val, uuid.UUID):
        return val
    try:
        return uuid.UUID(str(val))
    except (ValueError, TypeError, AttributeError):
        return None


def get_shelter_from_object(obj: Any) -> Optional[Shelter]:
    """Helper resolving Shelter instance from various domain model objects."""
    if obj is None:
        return None
    if isinstance(obj, Shelter):
        return obj
    if hasattr(obj, "shelter") and getattr(obj, "shelter", None) is not None:
        return getattr(obj, "shelter")
    if hasattr(obj, "verification") and getattr(obj, "verification", None) is not None:
        verification = getattr(obj, "verification")
        if verification and hasattr(verification, "shelter"):
            return getattr(verification, "shelter")
    return None


def get_active_member(user: Any, shelter: Optional[Shelter]) -> Optional[ShelterMember]:
    """Retrieves active member record for a user in a shelter."""
    if not user or not user.is_authenticated or not shelter:
        return None
    return ShelterMember.objects.filter(
        user=user, shelter=shelter, is_active=True
    ).first()


def is_system_administrator(user: Any) -> bool:
    """Checks if user is a system administrator or superuser."""
    if not user or not user.is_authenticated:
        return False
    if getattr(user, "is_superuser", False):
        return True
    from apps.accounts.services.authorization_service import AuthorizationService

    return AuthorizationService.has_role(user, RoleName.ADMINISTRATOR)


def is_verification_staff(user: Any) -> bool:
    """Checks if user has verification staff review privileges."""
    if not user or not user.is_authenticated:
        return False
    if is_system_administrator(user):
        return True
    if getattr(user, "is_staff", False):
        return True
    from apps.accounts.services.authorization_service import AuthorizationService

    return AuthorizationService.has_permission(user, "shelters.verify")


class IsShelterMember(BasePermission):
    """
    Permission class checking if user is an active member of the target shelter
    or possesses System Administrator privileges.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user) or is_verification_staff(request.user):
            return True
        pk = view.kwargs.get("pk")
        if pk:
            shelter_id = _to_uuid(pk)
            if shelter_id:
                shelter = Shelter.objects.filter(
                    id=shelter_id, is_deleted=False
                ).first()
                if shelter:
                    return self.has_object_permission(request, view, shelter)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user) or is_verification_staff(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        member = get_active_member(request.user, shelter)
        return member is not None


class IsShelterOwner(BasePermission):
    """
    Permission class checking if user is an active OWNER of the target shelter
    or possesses System Administrator privileges.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        pk = view.kwargs.get("pk")
        if pk:
            shelter_id = _to_uuid(pk)
            if shelter_id:
                shelter = Shelter.objects.filter(
                    id=shelter_id, is_deleted=False
                ).first()
                if shelter:
                    return self.has_object_permission(request, view, shelter)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        member = get_active_member(request.user, shelter)
        return member is not None and member.is_owner


class IsShelterManager(BasePermission):
    """
    Permission class checking if user is an active OWNER or MANAGER of the target shelter
    or possesses System Administrator privileges.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        pk = view.kwargs.get("pk")
        if pk:
            shelter_id = _to_uuid(pk)
            if shelter_id:
                shelter = Shelter.objects.filter(
                    id=shelter_id, is_deleted=False
                ).first()
                if shelter:
                    return self.has_object_permission(request, view, shelter)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        member = get_active_member(request.user, shelter)
        return member is not None and member.is_manager


class IsShelterStaff(BasePermission):
    """
    Permission class checking if user is an active OWNER, MANAGER, or STAFF of target shelter
    or possesses System Administrator privileges.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        pk = view.kwargs.get("pk")
        if pk:
            shelter_id = _to_uuid(pk)
            if shelter_id:
                shelter = Shelter.objects.filter(
                    id=shelter_id, is_deleted=False
                ).first()
                if shelter:
                    return self.has_object_permission(request, view, shelter)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        member = get_active_member(request.user, shelter)
        return member is not None and member.role in [
            ShelterMemberRole.OWNER,
            ShelterMemberRole.MANAGER,
            ShelterMemberRole.STAFF,
        ]


class CanManageShelter(BasePermission):
    """
    Permission class verifying authority to manage shelter profile and operational settings.
    Requires active OWNER or MANAGER role or System Administrator privileges.
    Denies access if shelter is archived unless user is System Administrator.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        pk = view.kwargs.get("pk")
        if pk:
            shelter_id = _to_uuid(pk)
            if shelter_id:
                shelter = Shelter.objects.filter(
                    id=shelter_id, is_deleted=False
                ).first()
                if shelter:
                    return self.has_object_permission(request, view, shelter)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        if shelter.status == ShelterStatus.ARCHIVED or not shelter.is_active:
            return False
        member = get_active_member(request.user, shelter)
        return member is not None and member.is_manager


class CanReviewVerification(BasePermission):
    """
    Permission class restricting verification workflow review actions (start-review, request-info,
    approve, reject) strictly to Verification Staff and System Administrators.
    Shelter Owners and Managers cannot approve/review their own shelter verifications.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return is_verification_staff(request.user)

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return is_verification_staff(request.user)


class CanInviteMembers(BasePermission):
    """
    Permission class authorizing user to issue staff/volunteer invitations or add members to shelter.
    Requires active OWNER or MANAGER role or System Administrator privileges.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        pk = view.kwargs.get("pk")
        if pk:
            shelter_id = _to_uuid(pk)
            if shelter_id:
                shelter = Shelter.objects.filter(
                    id=shelter_id, is_deleted=False
                ).first()
                if shelter:
                    return self.has_object_permission(request, view, shelter)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        if shelter.status == ShelterStatus.ARCHIVED or not shelter.is_active:
            return False
        member = get_active_member(request.user, shelter)
        return member is not None and member.is_manager


class CanTransferOwnership(BasePermission):
    """
    Permission class authorizing ownership transfers or modifications to OWNER role members.
    Requires active OWNER role or System Administrator privileges.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        pk = view.kwargs.get("pk")
        if pk:
            shelter_id = _to_uuid(pk)
            if shelter_id:
                shelter = Shelter.objects.filter(
                    id=shelter_id, is_deleted=False
                ).first()
                if shelter:
                    return self.has_object_permission(request, view, shelter)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        member = get_active_member(request.user, shelter)
        return member is not None and member.is_owner


class CanViewShelter(BasePermission):
    """
    Permission class for retrieving shelter details.
    Allows viewing active/verified shelters by any authenticated user.
    Inactive/archived shelters require active membership or System Administrator / Verification Staff role.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        pk = view.kwargs.get("pk")
        if pk:
            shelter_id = _to_uuid(pk)
            if shelter_id:
                shelter = Shelter.objects.filter(
                    id=shelter_id, is_deleted=False
                ).first()
                if shelter:
                    return self.has_object_permission(request, view, shelter)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user) or is_verification_staff(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        if shelter.status == ShelterStatus.ARCHIVED or not shelter.is_active:
            member = get_active_member(request.user, shelter)
            return member is not None
        return True


class CanDeleteDocument(BasePermission):
    """
    Permission class for deleting shelter verification documents.
    Requires active OWNER or MANAGER role or System Administrator privileges.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        doc_id = _to_uuid(view.kwargs.get("pk"))
        if doc_id:
            doc = ShelterDocument.objects.filter(id=doc_id).first()
            if doc:
                return self.has_object_permission(request, view, doc)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        member = get_active_member(request.user, shelter)
        return member is not None and member.is_manager


class CanManageMember(BasePermission):
    """
    Permission class for updating member roles or removing members from a shelter.
    Modifying/removing an OWNER requires active OWNER role or System Administrator.
    Modifying/removing MANAGER, STAFF, or VOLUNTEER requires active OWNER or MANAGER.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        mem_id = _to_uuid(view.kwargs.get("pk"))
        if mem_id:
            target_member = ShelterMember.objects.filter(id=mem_id).first()
            if target_member:
                return self.has_object_permission(request, view, target_member)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True

        target_member = obj if isinstance(obj, ShelterMember) else None
        if not target_member:
            return False

        shelter = target_member.shelter
        acting_member = get_active_member(request.user, shelter)
        if not acting_member:
            return False

        new_role = (
            (request.data.get("role") or "").lower()
            if hasattr(request, "data")
            else None
        )
        if target_member.is_owner or new_role == ShelterMemberRole.OWNER:
            return acting_member.is_owner

        return acting_member.is_manager


class CanRevokeInvitation(BasePermission):
    """
    Permission class for revoking pending shelter invitations.
    Requires active OWNER or MANAGER role or System Administrator privileges.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        inv_id_str = (
            request.data.get("invitation_id") if hasattr(request, "data") else None
        )
        inv_id = _to_uuid(inv_id_str) if inv_id_str else None
        if inv_id:
            inv = ShelterInvitation.objects.filter(id=inv_id).first()
            if inv:
                return self.has_object_permission(request, view, inv)
        return True

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if is_system_administrator(request.user):
            return True
        shelter = get_shelter_from_object(obj)
        if not shelter:
            return False
        member = get_active_member(request.user, shelter)
        return member is not None and member.is_manager

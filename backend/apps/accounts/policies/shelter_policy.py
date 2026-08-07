"""
Shelter domain policy implementation for PawMatch policy-based authorization.
"""

from typing import Any, Optional

from apps.accounts.policies.base_policy import BasePolicy
from apps.accounts.roles import RoleName
from apps.shelters.constants import ShelterStatus
from apps.shelters.models import Shelter, ShelterMember


def get_shelter_from_resource(resource: Any) -> Optional[Shelter]:
    """Helper resolving Shelter instance from resource object."""
    if resource is None:
        return None
    if isinstance(resource, Shelter):
        return resource
    if hasattr(resource, "shelter") and getattr(resource, "shelter", None) is not None:
        return getattr(resource, "shelter")
    if (
        hasattr(resource, "verification")
        and getattr(resource, "verification", None) is not None
    ):
        verification = getattr(resource, "verification")
        if verification and hasattr(verification, "shelter"):
            return getattr(verification, "shelter")
    return None


def get_active_member(user: Any, shelter: Optional[Shelter]) -> Optional[ShelterMember]:
    """Retrieves active member record for user in target shelter."""
    if not user or not user.is_authenticated or not shelter:
        return None
    return ShelterMember.objects.filter(
        user=user, shelter=shelter, is_active=True
    ).first()


def is_system_admin(user: Any) -> bool:
    """Checks whether user has System Administrator or superuser privileges."""
    if not user or not user.is_authenticated:
        return False
    if getattr(user, "is_superuser", False):
        return True
    from apps.accounts.services.authorization_service import AuthorizationService

    return AuthorizationService.has_role(user, RoleName.ADMINISTRATOR)


def is_verification_staff(user: Any) -> bool:
    """Checks whether user has verification reviewer privileges."""
    if not user or not user.is_authenticated:
        return False
    if is_system_admin(user):
        return True
    if getattr(user, "is_staff", False):
        return True
    from apps.accounts.services.authorization_service import AuthorizationService

    return AuthorizationService.has_permission(user, "shelters.verify")


class ShelterPolicy(BasePolicy):
    """
    Authorization policy evaluating access rules for Shelter entity and sub-resources.
    """

    def can_view(self, user: Any, target_object: Optional[Any] = None) -> bool:
        if not user or not user.is_authenticated:
            return False
        if is_system_admin(user):
            return True
        if target_object is None:
            return True
        shelter = get_shelter_from_resource(target_object)
        if not shelter:
            return True
        if shelter.status == ShelterStatus.ARCHIVED or not shelter.is_active:
            member = get_active_member(user, shelter)
            return member is not None
        return True

    def can_create(self, user: Any, target_object: Optional[Any] = None) -> bool:
        return bool(user and user.is_authenticated)

    def can_update(self, user: Any, target_object: Optional[Any] = None) -> bool:
        if not user or not user.is_authenticated:
            return False
        if is_system_admin(user):
            return True
        shelter = get_shelter_from_resource(target_object)
        if not shelter:
            return False
        if shelter.status == ShelterStatus.ARCHIVED or not shelter.is_active:
            return False
        member = get_active_member(user, shelter)
        return member is not None and member.is_manager

    def can_delete(self, user: Any, target_object: Optional[Any] = None) -> bool:
        if not user or not user.is_authenticated:
            return False
        if is_system_admin(user):
            return True
        shelter = get_shelter_from_resource(target_object)
        if not shelter:
            return False
        member = get_active_member(user, shelter)
        return member is not None and member.is_owner

    def can_manage(self, user: Any, target_object: Optional[Any] = None) -> bool:
        return self.can_update(user, target_object)

    def can_review_verification(
        self, user: Any, target_object: Optional[Any] = None
    ) -> bool:
        return is_verification_staff(user)

    def can_submit_verification(
        self, user: Any, target_object: Optional[Any] = None
    ) -> bool:
        return self.can_update(user, target_object)

    def can_invite_members(
        self, user: Any, target_object: Optional[Any] = None
    ) -> bool:
        return self.can_update(user, target_object)

    def can_transfer_ownership(
        self, user: Any, target_object: Optional[Any] = None
    ) -> bool:
        if not user or not user.is_authenticated:
            return False
        if is_system_admin(user):
            return True
        shelter = get_shelter_from_resource(target_object)
        if not shelter:
            return False
        member = get_active_member(user, shelter)
        return member is not None and member.is_owner

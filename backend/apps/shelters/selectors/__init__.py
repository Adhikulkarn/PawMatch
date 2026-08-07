"""
Selector layer exports for the Shelter bounded context.
Re-exports domain-specific query selector functions across shelter entities.
"""

from apps.shelters.selectors.invitation_selector import (
    get_invitation_by_token,
    get_pending_invitation_by_email,
    list_shelter_invitations,
)
from apps.shelters.selectors.member_selector import (
    get_shelter_members,
    get_shelter_owners,
    get_user_shelter_membership,
)
from apps.shelters.selectors.shelter_selector import (
    get_shelter_by_id,
    get_shelter_by_slug,
    get_shelters_by_status,
    list_all_shelters,
    list_verified_shelters,
    search_shelters,
)
from apps.shelters.selectors.verification_selector import (
    get_active_verification,
    get_verification_by_id,
    list_shelter_documents,
)

__all__ = [
    # Shelter Selectors
    "get_shelter_by_id",
    "get_shelter_by_slug",
    "list_verified_shelters",
    "list_all_shelters",
    "get_shelters_by_status",
    "search_shelters",
    # Member Selectors
    "get_shelter_members",
    "get_user_shelter_membership",
    "get_shelter_owners",
    # Verification & Document Selectors
    "get_active_verification",
    "get_verification_by_id",
    "list_shelter_documents",
    # Invitation Selectors
    "get_invitation_by_token",
    "get_pending_invitation_by_email",
    "list_shelter_invitations",
]

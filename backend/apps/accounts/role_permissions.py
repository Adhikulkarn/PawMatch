"""
Declarative Role-to-Permission mapping table for PawMatch RBAC.
"""

from typing import Dict, Set

from apps.accounts.permissions import PermissionName
from apps.accounts.roles import RoleName

ROLE_PERMISSIONS_MAP: Dict[str, Set[str]] = {
    RoleName.ADMINISTRATOR: PermissionName.get_all_permissions(),
    RoleName.SHELTER_MANAGER: {
        PermissionName.PETS_VIEW,
        PermissionName.PETS_CREATE,
        PermissionName.PETS_UPDATE,
        PermissionName.PETS_DELETE,
        PermissionName.PETS_ADOPT,
        PermissionName.SHELTERS_VIEW,
        PermissionName.SHELTERS_MANAGE,
        PermissionName.USERS_VIEW,
        PermissionName.MEDICAL_VIEW,
        PermissionName.REPORTS_VIEW,
        PermissionName.NOTIFICATIONS_SEND,
    },
    RoleName.SHELTER_STAFF: {
        PermissionName.PETS_VIEW,
        PermissionName.PETS_CREATE,
        PermissionName.PETS_UPDATE,
        PermissionName.SHELTERS_VIEW,
        PermissionName.MEDICAL_VIEW,
        PermissionName.NOTIFICATIONS_SEND,
    },
    RoleName.VETERINARIAN: {
        PermissionName.PETS_VIEW,
        PermissionName.MEDICAL_VIEW,
        PermissionName.MEDICAL_MANAGE,
        PermissionName.SHELTERS_VIEW,
    },
    RoleName.VOLUNTEER: {
        PermissionName.PETS_VIEW,
        PermissionName.PETS_UPDATE,
        PermissionName.SHELTERS_VIEW,
    },
    RoleName.ADOPTER: {
        PermissionName.PETS_VIEW,
        PermissionName.PETS_ADOPT,
        PermissionName.SHELTERS_VIEW,
    },
}


def get_permissions_for_role(role_name: str) -> Set[str]:
    """Returns set of permissions assigned to a given role name."""
    return ROLE_PERMISSIONS_MAP.get(role_name, set())

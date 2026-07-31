"""
Centralized permission definitions for PawMatch.
Defines platform-wide permission string constants.
"""


class PermissionName:
    """Centralized permission string constants."""

    # Pet Permissions
    PETS_VIEW = "pets.view"
    PETS_CREATE = "pets.create"
    PETS_UPDATE = "pets.update"
    PETS_DELETE = "pets.delete"
    PETS_ADOPT = "pets.adopt"

    # Shelter Permissions
    SHELTERS_VIEW = "shelters.view"
    SHELTERS_MANAGE = "shelters.manage"

    # User & Profile Permissions
    USERS_VIEW = "users.view"
    USERS_MANAGE = "users.manage"

    # Medical Record Permissions
    MEDICAL_VIEW = "medical.view"
    MEDICAL_MANAGE = "medical.manage"

    # System & Report Permissions
    REPORTS_VIEW = "reports.view"
    NOTIFICATIONS_SEND = "notifications.send"

    @classmethod
    def get_all_permissions(cls) -> set:
        """Returns set of all defined permission strings."""
        return {
            val
            for key, val in cls.__dict__.items()
            if not key.startswith("_") and isinstance(val, str)
        }

"""
Platform role definitions for PawMatch RBAC subsystem.
"""


class RoleName:
    """Centralized platform role constants."""

    ADMINISTRATOR = "ADMINISTRATOR"
    SHELTER_MANAGER = "SHELTER_MANAGER"
    SHELTER_STAFF = "SHELTER_STAFF"
    VETERINARIAN = "VETERINARIAN"
    VOLUNTEER = "VOLUNTEER"
    ADOPTER = "ADOPTER"

    @classmethod
    def get_all_roles(cls) -> set:
        """Returns set of all defined platform role strings."""
        return {
            val
            for key, val in cls.__dict__.items()
            if not key.startswith("_") and isinstance(val, str)
        }

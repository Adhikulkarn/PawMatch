"""
Pet resource authorization policy for PawMatch.
Demonstrates object-level ownership and shelter multi-tenant isolation rules.
"""

from typing import Any, Optional

from apps.accounts.policies.base_policy import BasePolicy


class PetPolicy(BasePolicy):
    """Policy governing authorization rules for Pet objects and shelter isolation."""

    def can_view(self, user: Any, target_object: Optional[Any] = None) -> bool:
        return True

    def can_create(self, user: Any, target_object: Optional[Any] = None) -> bool:
        if not user or not user.is_authenticated:
            return False
        return user.is_staff or user.is_superuser

    def can_update(self, user: Any, target_object: Optional[Any] = None) -> bool:
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True

        if target_object is None:
            return True

        # Check object-level shelter ownership if both specify shelter_id
        if hasattr(target_object, "shelter_id") and hasattr(user, "shelter_id"):
            if target_object.shelter_id and user.shelter_id:
                return str(target_object.shelter_id) == str(user.shelter_id)

        # Check direct owner ownership
        if hasattr(target_object, "owner_id") and target_object.owner_id:
            return str(target_object.owner_id) == str(user.id)

        return user.is_staff

    def can_delete(self, user: Any, target_object: Optional[Any] = None) -> bool:
        return self.can_update(user, target_object)

"""
User resource authorization policy for PawMatch.
"""

from typing import Any, Optional

from apps.accounts.policies.base_policy import BasePolicy


class UserPolicy(BasePolicy):
    """Policy governing authorization rules for User and UserProfile resources."""

    def can_view(self, user: Any, target_object: Optional[Any] = None) -> bool:
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        if target_object is None:
            return True
        target_user_id = (
            target_object.user.id
            if hasattr(target_object, "user")
            else getattr(target_object, "id", None)
        )
        return user.id == target_user_id

    def can_update(self, user: Any, target_object: Optional[Any] = None) -> bool:
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if target_object is None:
            return True
        target_user_id = (
            target_object.user.id
            if hasattr(target_object, "user")
            else getattr(target_object, "id", None)
        )
        return user.id == target_user_id

    def can_delete(self, user: Any, target_object: Optional[Any] = None) -> bool:
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        target_user_id = (
            target_object.user.id
            if hasattr(target_object, "user")
            else getattr(target_object, "id", None)
        )
        return user.id == target_user_id

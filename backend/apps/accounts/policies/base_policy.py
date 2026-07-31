"""
Abstract Base Policy definition for PawMatch policy-based authorization engine.
"""

from abc import ABC
from typing import Any, Optional


class BasePolicy(ABC):
    """
    Abstract policy interface for resource authorization evaluation.
    Subclasses evaluate user identity, role, and resource ownership rules.
    """

    def can_view(self, user: Any, target_object: Optional[Any] = None) -> bool:
        """Evaluates whether user can view target object."""
        return True

    def can_create(self, user: Any, target_object: Optional[Any] = None) -> bool:
        """Evaluates whether user can create target object."""
        return True

    def can_update(self, user: Any, target_object: Optional[Any] = None) -> bool:
        """Evaluates whether user can update target object."""
        return True

    def can_delete(self, user: Any, target_object: Optional[Any] = None) -> bool:
        """Evaluates whether user can delete target object."""
        return True

    def can_action(
        self, action: str, user: Any, target_object: Optional[Any] = None
    ) -> bool:
        """Generic action dispatcher method."""
        method_name = action if action.startswith("can_") else f"can_{action}"
        if hasattr(self, method_name):
            handler = getattr(self, method_name)
            return handler(user, target_object)
        return False

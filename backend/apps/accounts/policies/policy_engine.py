"""
Policy Engine for PawMatch authorization framework.
Resolves and executes resource policy rules dynamically.
"""

from typing import Any, Dict, Optional, Type

from apps.accounts.models import User, UserProfile
from apps.accounts.policies.base_policy import BasePolicy
from apps.accounts.policies.pet_policy import PetPolicy
from apps.accounts.policies.user_policy import UserPolicy


class PolicyEngine:
    """
    Central Policy Engine resolving policies for resource models/objects.
    """

    _registry: Dict[Any, Type[BasePolicy]] = {
        User: UserPolicy,
        UserProfile: UserPolicy,
        "user": UserPolicy,
        "pet": PetPolicy,
    }

    @classmethod
    def register_policy(cls, resource_key: Any, policy_cls: Type[BasePolicy]) -> None:
        """Registers a policy class for a resource type or key."""
        cls._registry[resource_key] = policy_cls

    @classmethod
    def resolve_policy(cls, resource: Any) -> Optional[BasePolicy]:
        """Resolves policy instance for model class, string key, or model instance."""
        if resource is None:
            return None

        # 1. Check explicit _policy_type attribute
        if hasattr(resource, "_policy_type"):
            policy_key = getattr(resource, "_policy_type")
            if policy_key in cls._registry:
                return cls._registry[policy_key]()

        # 2. Direct key lookup (handling unhashable instances)
        try:
            if resource in cls._registry:
                policy_cls = cls._registry[resource]
                return policy_cls()
        except TypeError:
            pass

        # 3. Instance class lookup
        resource_cls = resource if isinstance(resource, type) else resource.__class__
        try:
            if resource_cls in cls._registry:
                policy_cls = cls._registry[resource_cls]
                return policy_cls()
        except TypeError:
            pass

        # 4. String type name lookup
        type_name = resource_cls.__name__.lower()
        if type_name in cls._registry:
            policy_cls = cls._registry[type_name]
            return policy_cls()

        return None

    @classmethod
    def evaluate(
        cls, user: Any, action: str, resource: Optional[Any] = None
    ) -> bool:
        """
        Evaluates authorization policy for user, action, and target resource object.
        """
        policy = cls.resolve_policy(resource)
        if policy is None:
            return False
        return policy.can_action(action, user, resource)

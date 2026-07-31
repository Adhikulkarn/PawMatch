"""
Authorization decorators for view functions and service methods in PawMatch.
"""

from functools import wraps
from typing import Callable

from apps.accounts.services.authorization_service import AuthorizationService


def require_permission(permission_name: str) -> Callable:
    """
    Decorator enforcing that the executing user possesses the specified permission string.
    Works for view methods (request in args) or service functions (user in args/kwargs).
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = None
            user = None

            # Extract request or user object from arguments
            for arg in args:
                if hasattr(arg, "user"):
                    request = arg
                    user = getattr(arg, "user", None)
                    break
                elif hasattr(arg, "is_authenticated"):
                    user = arg
                    break

            if user is None:
                user = kwargs.get("user")

            AuthorizationService.authorize(
                user=user,
                permission_or_action=permission_name,
                request=request,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_role(role_name: str) -> Callable:
    """
    Decorator enforcing that the executing user possesses the specified platform role.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = None
            user = None

            for arg in args:
                if hasattr(arg, "user"):
                    request = arg
                    user = getattr(arg, "user", None)
                    break
                elif hasattr(arg, "is_authenticated"):
                    user = arg
                    break

            if user is None:
                user = kwargs.get("user")

            if not AuthorizationService.has_role(user, role_name):
                AuthorizationService.authorize(
                    user=user,
                    permission_or_action=role_name,
                    request=request,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator

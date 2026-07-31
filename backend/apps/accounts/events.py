"""
Event-driven authentication, profile & authorization module for PawMatch Accounts.
Provides lightweight event classes and signal handlers to decouple side-effects
(Audit Logging, Email Notifications, Media Storage, Analytics) from core domain services.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from django.dispatch import Signal

# Django Signals for Authentication, Profile, Password & Authorization Events
user_registered_signal = Signal()
email_verified_signal = Signal()
user_logged_in_signal = Signal()
user_logged_out_signal = Signal()
profile_updated_signal = Signal()
avatar_uploaded_signal = Signal()
avatar_deleted_signal = Signal()
account_deactivated_signal = Signal()
password_reset_requested_signal = Signal()
password_reset_completed_signal = Signal()
password_changed_signal = Signal()
permission_granted_signal = Signal()
permission_denied_signal = Signal()
role_assigned_signal = Signal()
role_removed_signal = Signal()
role_replaced_signal = Signal()


@dataclass
class UserRegisteredEvent:
    user_id: Any
    email: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class EmailVerifiedEvent:
    user_id: Any
    email: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class UserLoggedInEvent:
    user_id: Any
    email: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class UserLoggedOutEvent:
    user_id: Optional[Any]
    email: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ProfileUpdatedEvent:
    user_id: Any
    email: str
    updated_fields: list
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AvatarUploadedEvent:
    user_id: Any
    email: str
    avatar_url: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AvatarDeletedEvent:
    user_id: Any
    email: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AccountDeactivatedEvent:
    user_id: Any
    email: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PasswordResetRequestedEvent:
    user_id: Any
    email: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PasswordResetCompletedEvent:
    user_id: Any
    email: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PasswordChangedEvent:
    user_id: Any
    email: str
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PermissionGrantedEvent:
    user_id: Any
    email: str
    permission: str
    resource: Optional[Any] = None
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PermissionDeniedEvent:
    user_id: Any
    email: str
    permission: str
    resource: Optional[Any] = None
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class RoleAssignedEvent:
    user_id: Any
    email: str
    role_name: str
    assigned_by: Optional[Any] = None
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class RoleRemovedEvent:
    user_id: Any
    email: str
    role_name: str
    removed_by: Optional[Any] = None
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class RoleReplacedEvent:
    user_id: Any
    email: str
    roles: list
    replaced_by: Optional[Any] = None
    request: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EventDispatcher:
    """Dispatches authentication, profile, password & authorization events to connected listeners."""

    @staticmethod
    def dispatch_user_registered(
        user_id: Any, email: str, request: Optional[Any] = None
    ) -> None:
        event = UserRegisteredEvent(user_id=user_id, email=email, request=request)
        user_registered_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_email_verified(
        user_id: Any, email: str, request: Optional[Any] = None
    ) -> None:
        event = EmailVerifiedEvent(user_id=user_id, email=email, request=request)
        email_verified_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_user_logged_in(
        user_id: Any, email: str, request: Optional[Any] = None
    ) -> None:
        event = UserLoggedInEvent(user_id=user_id, email=email, request=request)
        user_logged_in_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_user_logged_out(
        user_id: Optional[Any], email: str, request: Optional[Any] = None
    ) -> None:
        event = UserLoggedOutEvent(user_id=user_id, email=email, request=request)
        user_logged_out_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_profile_updated(
        user_id: Any, email: str, updated_fields: list, request: Optional[Any] = None
    ) -> None:
        event = ProfileUpdatedEvent(
            user_id=user_id, email=email, updated_fields=updated_fields, request=request
        )
        profile_updated_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_avatar_uploaded(
        user_id: Any, email: str, avatar_url: str, request: Optional[Any] = None
    ) -> None:
        event = AvatarUploadedEvent(
            user_id=user_id, email=email, avatar_url=avatar_url, request=request
        )
        avatar_uploaded_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_avatar_deleted(
        user_id: Any, email: str, request: Optional[Any] = None
    ) -> None:
        event = AvatarDeletedEvent(user_id=user_id, email=email, request=request)
        avatar_deleted_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_account_deactivated(
        user_id: Any, email: str, request: Optional[Any] = None
    ) -> None:
        event = AccountDeactivatedEvent(user_id=user_id, email=email, request=request)
        account_deactivated_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_password_reset_requested(
        user_id: Any, email: str, request: Optional[Any] = None
    ) -> None:
        event = PasswordResetRequestedEvent(
            user_id=user_id, email=email, request=request
        )
        password_reset_requested_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_password_reset_completed(
        user_id: Any, email: str, request: Optional[Any] = None
    ) -> None:
        event = PasswordResetCompletedEvent(
            user_id=user_id, email=email, request=request
        )
        password_reset_completed_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_password_changed(
        user_id: Any, email: str, request: Optional[Any] = None
    ) -> None:
        event = PasswordChangedEvent(user_id=user_id, email=email, request=request)
        password_changed_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_permission_granted(
        user_id: Any,
        email: str,
        permission: str,
        resource: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> None:
        event = PermissionGrantedEvent(
            user_id=user_id,
            email=email,
            permission=permission,
            resource=resource,
            request=request,
        )
        permission_granted_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_permission_denied(
        user_id: Any,
        email: str,
        permission: str,
        resource: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> None:
        event = PermissionDeniedEvent(
            user_id=user_id,
            email=email,
            permission=permission,
            resource=resource,
            request=request,
        )
        permission_denied_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_role_assigned(
        user_id: Any,
        email: str,
        role_name: str,
        assigned_by: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> None:
        event = RoleAssignedEvent(
            user_id=user_id,
            email=email,
            role_name=role_name,
            assigned_by=assigned_by,
            request=request,
        )
        role_assigned_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_role_removed(
        user_id: Any,
        email: str,
        role_name: str,
        removed_by: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> None:
        event = RoleRemovedEvent(
            user_id=user_id,
            email=email,
            role_name=role_name,
            removed_by=removed_by,
            request=request,
        )
        role_removed_signal.send(sender=EventDispatcher, event=event)

    @staticmethod
    def dispatch_role_replaced(
        user_id: Any,
        email: str,
        roles: list,
        replaced_by: Optional[Any] = None,
        request: Optional[Any] = None,
    ) -> None:
        event = RoleReplacedEvent(
            user_id=user_id,
            email=email,
            roles=roles,
            replaced_by=replaced_by,
            request=request,
        )
        role_replaced_signal.send(sender=EventDispatcher, event=event)

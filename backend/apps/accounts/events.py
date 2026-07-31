"""
Event-driven authentication module for PawMatch Accounts.
Provides lightweight event classes and signal handlers to decouple side-effects
(Audit Logging, Email Notifications) from core domain services.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from django.dispatch import Signal

# Django Signals for Authentication Events
user_registered_signal = Signal()
email_verified_signal = Signal()
user_logged_in_signal = Signal()
user_logged_out_signal = Signal()


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


class EventDispatcher:
    """Dispatches authentication events to connected listeners."""

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

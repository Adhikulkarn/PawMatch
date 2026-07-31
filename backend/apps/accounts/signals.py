"""
Django signals for Accounts module.
Handles automatic UserProfile creation and optional post_migrate RBAC synchronization.
"""

from typing import Any

from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from apps.accounts.config import accounts_config
from apps.accounts.models.profile import UserProfile
from apps.accounts.models.user import User


@receiver(post_save, sender=User)
def create_user_profile_signal(
    sender: Any, instance: User, created: bool, **kwargs: Any
) -> None:
    """Ensures every newly created User instance receives a UserProfile."""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_migrate)
def sync_rbac_post_migrate_signal(sender: Any, **kwargs: Any) -> None:
    """
    Optional post_migrate signal handler to automatically synchronize RBAC after migrations.
    Controlled by accounts_config.enable_auto_rbac_sync setting (default: False).
    The official synchronization mechanism remains `python manage.py sync_rbac`.
    """
    if getattr(accounts_config, "enable_auto_rbac_sync", False):
        if hasattr(sender, "name") and sender.name == "apps.accounts":
            from apps.accounts.services.rbac_service import RBACService

            RBACService.sync()

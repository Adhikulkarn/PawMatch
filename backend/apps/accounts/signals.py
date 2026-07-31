"""
Django post_save signals for Accounts module.
Automatically creates a UserProfile instance whenever a new User is created.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models.profile import UserProfile
from apps.accounts.models.user import User


@receiver(post_save, sender=User)
def create_user_profile_signal(sender, instance: User, created: bool, **kwargs):
    """Ensures every newly created User instance receives a UserProfile."""
    if created:
        UserProfile.objects.get_or_create(user=instance)

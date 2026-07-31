"""
Django management command to execute RBAC role & permission synchronization.
Usage: python manage.py sync_rbac
"""

from typing import Any

from django.core.management.base import BaseCommand

from apps.accounts.services.rbac_service import RBACService


class Command(BaseCommand):
    """
    Management command to synchronize platform roles, permissions, and group mappings
    with Django Groups & Permissions.
    """

    help = (
        "Synchronizes platform RBAC roles, permissions, and group mappings "
        "with Django Groups & Permissions."
    )

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write("Starting RBAC Role & Permission Synchronization...\n")

        try:
            result = RBACService.sync()

            for group_name, details in result["roles"].items():
                perm_count = details["permission_count"]
                self.stdout.write(
                    self.style.SUCCESS(f"✓ {group_name}")
                    + f"\n  → {perm_count} permissions\n"
                )

            self.stdout.write(self.style.SUCCESS("Synchronization Complete"))
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"RBAC Synchronization Failed: {exc}"))
            raise

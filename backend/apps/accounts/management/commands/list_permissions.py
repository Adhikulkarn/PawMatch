"""
Django management command to list all platform permissions categorized by domain.
Usage: python manage.py list_permissions
"""

from collections import defaultdict
from typing import Any

from django.core.management.base import BaseCommand

from apps.accounts.permissions import PermissionName


class Command(BaseCommand):
    """
    Management command displaying all registered platform permissions categorized by domain namespace.
    """

    help = "Lists all platform permission strings categorized by domain module."

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write(
            self.style.MIGRATE_HEADING("\n=== PawMatch Platform Permissions ===")
        )

        all_perms = sorted(list(PermissionName.get_all_permissions()))
        categorized: dict[str, list[str]] = defaultdict(list)

        for perm in all_perms:
            prefix = perm.split(".")[0] if "." in perm else "global"
            categorized[prefix].append(perm)

        for category in sorted(categorized.keys()):
            perms = categorized[category]
            self.stdout.write(
                self.style.SUCCESS(f"\n[{category.upper()} Domain ({len(perms)})]")
            )
            for p in perms:
                self.stdout.write(f"  - {p}")

        self.stdout.write(
            self.style.SUCCESS(f"\nTotal Platform Permissions: {len(all_perms)}\n")
        )

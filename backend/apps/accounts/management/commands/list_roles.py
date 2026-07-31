"""
Django management command to list all platform RBAC roles, display names, and permission counts.
Usage: python manage.py list_roles
"""

from typing import Any

from django.core.management.base import BaseCommand

from apps.accounts.role_permissions import get_permissions_for_role
from apps.accounts.roles import RoleName
from apps.accounts.services.rbac_service import RBACService


class Command(BaseCommand):
    """
    Management command displaying a detailed summary of defined platform roles,
    their mapped Django Group names, and assigned permissions count.
    """

    help = "Lists all defined platform roles, display names, and mapped permissions."

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write(
            self.style.MIGRATE_HEADING("\n=== PawMatch Platform Roles ===")
        )

        all_roles = sorted(list(RoleName.get_all_roles()))

        for role_name in all_roles:
            group_name = RBACService.get_group_name_for_role(role_name)
            permissions = sorted(list(get_permissions_for_role(role_name)))
            perm_count = len(permissions)

            self.stdout.write(
                self.style.SUCCESS(f"\n[Role: {role_name}]")
                + f" (Display: '{group_name}')"
            )
            self.stdout.write(f"  Total Permissions: {perm_count}")

            if permissions:
                self.stdout.write("  Permissions:")
                for p in permissions:
                    self.stdout.write(f"    - {p}")

        self.stdout.write(
            self.style.SUCCESS(f"\nTotal Roles Listed: {len(all_roles)}\n")
        )

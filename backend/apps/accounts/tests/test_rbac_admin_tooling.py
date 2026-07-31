"""
Comprehensive test suite for Phase 1.6.6 Django Admin & RBAC Tooling.
Tests management commands (sync_rbac, list_roles, list_permissions) and Admin UI display helpers.
"""

from io import StringIO

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase

from apps.accounts.admin import EnhancedGroupAdmin, UserAdmin
from apps.accounts.roles import RoleName
from apps.accounts.services.rbac_service import RBACService
from apps.accounts.services.role_service import RoleService

User = get_user_model()


class RBACAdminToolingTestCase(TestCase):
    """Test suite for RBAC CLI management commands and Django Admin customizations."""

    def setUp(self):
        # Synchronize RBAC infrastructure before each test
        RBACService.sync()

        self.admin_site = AdminSite()
        self.group_admin = EnhancedGroupAdmin(Group, self.admin_site)
        self.user_admin = UserAdmin(User, self.admin_site)

        self.user = User.objects.create_user(
            email="staff@pawmatch.org",
            password="Password123!",
            first_name="Staff",
            last_name="User",
        )
        RoleService.assign_role(self.user, RoleName.SHELTER_STAFF)

    def test_sync_rbac_command(self):
        """Verifies sync_rbac management command executes cleanly."""
        out = StringIO()
        call_command("sync_rbac", stdout=out)
        output = out.getvalue()

        self.assertIn("Starting RBAC Role & Permission Synchronization", output)
        self.assertIn("Synchronization Complete", output)

    def test_list_roles_command(self):
        """Verifies list_roles management command displays platform role registry."""
        out = StringIO()
        call_command("list_roles", stdout=out)
        output = out.getvalue()

        self.assertIn("PawMatch Platform Roles", output)
        self.assertIn("[Role: ADMINISTRATOR]", output)
        self.assertIn("[Role: SHELTER_MANAGER]", output)
        self.assertIn("Total Roles Listed: 6", output)

    def test_list_permissions_command(self):
        """Verifies list_permissions management command displays domain-categorized permissions."""
        out = StringIO()
        call_command("list_permissions", stdout=out)
        output = out.getvalue()

        self.assertIn("PawMatch Platform Permissions", output)
        self.assertIn("PETS Domain", output)
        self.assertIn("SHELTERS Domain", output)
        self.assertIn("Total Platform Permissions: 13", output)

    def test_enhanced_group_admin_display_methods(self):
        """Verifies EnhancedGroupAdmin display methods (role_code_display, permission_count)."""
        group = Group.objects.get(name="Shelter Staff")

        role_code_html = self.group_admin.role_code_display(group)
        self.assertIn("SHELTER_STAFF", role_code_html)

        perm_count = self.group_admin.permission_count(group)
        self.assertGreater(perm_count, 0)

    def test_user_admin_rbac_display_methods(self):
        """Verifies UserAdmin display methods for assigned roles and permissions."""
        roles_text = self.user_admin.roles_display(self.user)
        self.assertIn(RoleName.SHELTER_STAFF, roles_text)

        roles_summary_html = self.user_admin.roles_summary_display(self.user)
        self.assertIn(RoleName.SHELTER_STAFF, roles_summary_html)

        perms_summary_html = self.user_admin.permissions_summary_display(self.user)
        self.assertIn("pets.create", perms_summary_html)

"""
Comprehensive test suite for Phase 1.6.1 RBAC Role & Permission Synchronization.
"""

from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.db import DatabaseError
from django.test import TestCase

from apps.accounts.constants import AuditAction
from apps.accounts.permissions import PermissionName
from apps.accounts.role_permissions import get_permissions_for_role
from apps.accounts.services.rbac_service import ROLE_TO_GROUP_NAME, RBACService
from apps.audit_logs.models import AuditLog

User = get_user_model()


class RBACSyncServiceTest(TestCase):
    """Test suite for RBACService synchronization functionality."""

    def test_sync_creates_all_groups(self):
        """Verifies that running sync creates all expected Django Groups."""
        result = RBACService.sync()

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["roles_synchronized"], 6)

        for role_name, group_name in ROLE_TO_GROUP_NAME.items():
            self.assertTrue(
                Group.objects.filter(name=group_name).exists(),
                f"Group '{group_name}' for role '{role_name}' was not created.",
            )

    def test_sync_creates_all_permissions(self):
        """Verifies that running sync creates all defined PermissionName constants."""
        all_expected_perms = PermissionName.get_all_permissions()

        result = RBACService.sync()

        self.assertEqual(result["permissions_synchronized"], len(all_expected_perms))

        for perm_str in all_expected_perms:
            app_label, codename = perm_str.split(".", 1)
            self.assertTrue(
                Permission.objects.filter(
                    content_type__app_label=app_label, codename=codename
                ).exists(),
                f"Permission '{perm_str}' was not created in Permission table.",
            )

    def test_role_permission_mappings(self):
        """Verifies that each group receives exact permission mappings from ROLE_PERMISSIONS_MAP."""
        RBACService.sync()

        for role_name, group_name in ROLE_TO_GROUP_NAME.items():
            group = Group.objects.get(name=group_name)
            assigned_perms = {
                f"{p.content_type.app_label}.{p.codename}"
                for p in group.permissions.all()
            }
            expected_perms = get_permissions_for_role(role_name)

            self.assertEqual(
                assigned_perms,
                expected_perms,
                f"Permission mismatch for group '{group_name}'.",
            )

    def test_sync_idempotency(self):
        """Verifies that running sync multiple times is idempotent and produces no duplicates."""
        initial_result = RBACService.sync()
        initial_group_count = Group.objects.count()
        initial_perm_count = Permission.objects.count()

        second_result = RBACService.sync()

        self.assertEqual(Group.objects.count(), initial_group_count)
        self.assertEqual(Permission.objects.count(), initial_perm_count)
        self.assertEqual(
            second_result["roles_synchronized"], initial_result["roles_synchronized"]
        )
        self.assertEqual(
            second_result["permissions_synchronized"],
            initial_result["permissions_synchronized"],
        )

    def test_sync_removes_stale_permissions(self):
        """Verifies that sync automatically removes permissions removed from role definitions."""
        RBACService.sync()

        shelter_staff_group = Group.objects.get(name="Shelter Staff")
        extra_perm = Permission.objects.create(
            codename="extra_stale_perm",
            content_type=Permission.objects.first().content_type,
            name="Extra Stale Permission",
        )
        shelter_staff_group.permissions.add(extra_perm)

        self.assertIn(extra_perm, shelter_staff_group.permissions.all())

        # Re-run sync to strip stale permissions
        RBACService.sync()

        self.assertNotIn(extra_perm, shelter_staff_group.permissions.all())

    def test_transaction_rollback_on_failure(self):
        """Verifies that database failures roll back changes and log failure events."""
        with patch.object(
            RBACService,
            "sync_groups_and_mappings",
            side_effect=DatabaseError("Simulated DB connection failure"),
        ):
            with self.assertRaises(DatabaseError):
                RBACService.sync()

        # Verify failure audit log entry was created
        failed_audit = AuditLog.objects.filter(
            action=AuditAction.RBAC_SYNC_FAILED
        ).first()
        self.assertIsNotNone(failed_audit)
        self.assertEqual(failed_audit.status, "FAILED")
        self.assertIn("Simulated DB connection failure", failed_audit.details["error"])

    def test_user_has_perm_integration(self):
        """Verifies that users added to synchronized groups inherit native Django permissions."""
        RBACService.sync()

        user = User.objects.create_user(
            email="staff@pawmatch.org",
            password="Password123!",
            first_name="Staff",
            last_name="Member",
        )
        group = Group.objects.get(name="Shelter Staff")
        user.groups.add(group)

        # Shelter staff should have pets.create permission
        self.assertTrue(user.has_perm("pets.create"))
        # Shelter staff should NOT have pets.delete permission
        self.assertFalse(user.has_perm("pets.delete"))

    def test_audit_logs_recorded(self):
        """Verifies that RBAC_SYNC_STARTED and RBAC_SYNC_COMPLETED audit logs are created."""
        RBACService.sync()

        started_log = AuditLog.objects.filter(
            action=AuditAction.RBAC_SYNC_STARTED
        ).first()
        completed_log = AuditLog.objects.filter(
            action=AuditAction.RBAC_SYNC_COMPLETED
        ).first()

        self.assertIsNotNone(started_log)
        self.assertIsNotNone(completed_log)
        self.assertEqual(started_log.status, "SUCCESS")
        self.assertEqual(completed_log.status, "SUCCESS")
        self.assertEqual(completed_log.details["roles_synchronized"], 6)


class SyncRBACManagementCommandTest(TestCase):
    """Test suite for sync_rbac Django management command."""

    def test_management_command_output(self):
        """Verifies that running 'python manage.py sync_rbac' outputs summary and succeeds."""
        out = StringIO()
        call_command("sync_rbac", stdout=out)

        output_text = out.getvalue()
        self.assertIn("Starting RBAC Role & Permission Synchronization", output_text)
        self.assertIn("✓ Administrator", output_text)
        self.assertIn("✓ Shelter Manager", output_text)
        self.assertIn("✓ Shelter Staff", output_text)
        self.assertIn("✓ Veterinarian", output_text)
        self.assertIn("✓ Volunteer", output_text)
        self.assertIn("✓ Adopter", output_text)
        self.assertIn("Synchronization Complete", output_text)

    def test_management_command_failure_handling(self):
        """Verifies management command output on sync failure."""
        err = StringIO()
        with patch.object(
            RBACService,
            "sync",
            side_effect=RuntimeError("System error during sync"),
        ):
            with self.assertRaises(RuntimeError):
                call_command("sync_rbac", stderr=err)

        err_text = err.getvalue()
        self.assertIn("RBAC Synchronization Failed", err_text)

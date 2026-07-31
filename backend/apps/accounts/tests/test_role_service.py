"""
Comprehensive test suite for Phase 1.6.2 Role Assignment Service (RoleService).
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from apps.accounts.constants import AuditAction
from apps.accounts.exceptions import (
    DuplicateRoleException,
    InvalidRoleException,
    RoleNotAssignedException,
)
from apps.accounts.permissions import PermissionName
from apps.accounts.role_permissions import get_permissions_for_role
from apps.accounts.roles import RoleName
from apps.accounts.services.rbac_service import RBACService
from apps.accounts.services.role_service import RoleService
from apps.audit_logs.models import AuditLog

User = get_user_model()


class RoleServiceTest(TestCase):
    """Test suite for RoleService role management operations."""

    def setUp(self):
        # Synchronize RBAC infrastructure before each test
        RBACService.sync()

        self.user = User.objects.create_user(
            email="user@pawmatch.org",
            password="Password123!",
            first_name="Test",
            last_name="User",
        )
        self.actor = User.objects.create_user(
            email="admin@pawmatch.org",
            password="Password123!",
            first_name="Admin",
            last_name="Actor",
            is_staff=True,
            is_superuser=True,
        )

    def test_assign_role_success(self):
        """Verifies assigning a valid role updates user groups, user.role, and logs audit events."""
        updated_user = RoleService.assign_role(
            user=self.user, role=RoleName.SHELTER_MANAGER, actor=self.actor
        )

        self.assertTrue(RoleService.has_role(updated_user, RoleName.SHELTER_MANAGER))
        group = Group.objects.get(name="Shelter Manager")
        self.assertIn(group, updated_user.groups.all())

        # Check Audit Log
        audit = AuditLog.objects.filter(
            user_id=self.user.id, action=AuditAction.ROLE_ASSIGNED
        ).first()
        self.assertIsNotNone(audit)
        self.assertEqual(audit.details["role"], RoleName.SHELTER_MANAGER)
        self.assertEqual(audit.details["assigned_by"], str(self.actor.id))

    def test_assign_invalid_role_raises_exception(self):
        """Verifies that assigning an invalid role string raises InvalidRoleException."""
        with self.assertRaises(InvalidRoleException):
            RoleService.assign_role(user=self.user, role="INVALID_ROLE_NAME")

    def test_assign_duplicate_role_raises_exception(self):
        """Verifies that assigning an already possessed role raises DuplicateRoleException."""
        RoleService.assign_role(user=self.user, role=RoleName.VETERINARIAN)

        with self.assertRaises(DuplicateRoleException):
            RoleService.assign_role(user=self.user, role=RoleName.VETERINARIAN)

    def test_remove_role_success(self):
        """Verifies removing a role removes group membership, updates role, and logs audit event."""
        RoleService.assign_role(user=self.user, role=RoleName.VOLUNTEER)
        self.assertTrue(RoleService.has_role(self.user, RoleName.VOLUNTEER))

        RoleService.remove_role(
            user=self.user, role=RoleName.VOLUNTEER, actor=self.actor
        )

        self.assertFalse(RoleService.has_role(self.user, RoleName.VOLUNTEER))
        group = Group.objects.get(name="Volunteer")
        self.assertNotIn(group, self.user.groups.all())

        audit = AuditLog.objects.filter(
            user_id=self.user.id, action=AuditAction.ROLE_REMOVED
        ).first()
        self.assertIsNotNone(audit)
        self.assertEqual(audit.details["role"], RoleName.VOLUNTEER)

    def test_remove_unassigned_role_raises_exception(self):
        """Verifies attempting to remove an unassigned role raises RoleNotAssignedException."""
        with self.assertRaises(RoleNotAssignedException):
            RoleService.remove_role(user=self.user, role=RoleName.VETERINARIAN)

    def test_remove_invalid_role_raises_exception(self):
        """Verifies attempting to remove an invalid role raises InvalidRoleException."""
        with self.assertRaises(InvalidRoleException):
            RoleService.remove_role(user=self.user, role="NON_EXISTENT_ROLE")

    def test_replace_roles_success(self):
        """Verifies replacing user roles with a new set of roles."""
        RoleService.assign_role(user=self.user, role=RoleName.ADOPTER)

        new_roles = [RoleName.SHELTER_MANAGER, RoleName.VETERINARIAN]
        updated_user = RoleService.replace_roles(
            user=self.user, roles=new_roles, actor=self.actor
        )

        user_roles = RoleService.get_roles(updated_user)
        self.assertIn(RoleName.SHELTER_MANAGER, user_roles)
        self.assertIn(RoleName.VETERINARIAN, user_roles)

        audit = AuditLog.objects.filter(
            user_id=self.user.id, action=AuditAction.ROLE_REPLACED
        ).first()
        self.assertIsNotNone(audit)
        self.assertEqual(sorted(audit.details["roles"]), sorted(new_roles))

    def test_replace_roles_invalid_role_raises_exception(self):
        """Verifies replacing roles with an invalid role raises InvalidRoleException."""
        with self.assertRaises(InvalidRoleException):
            RoleService.replace_roles(
                user=self.user, roles=[RoleName.SHELTER_STAFF, "BAD_ROLE"]
            )

    def test_clear_roles(self):
        """Verifies clearing all user roles."""
        RoleService.assign_role(user=self.user, role=RoleName.VOLUNTEER)
        self.assertTrue(len(RoleService.get_roles(self.user)) > 0)

        RoleService.clear_roles(user=self.user, actor=self.actor)

        self.assertEqual(len(self.user.groups.all()), 0)

    def test_multiple_roles_permission_aggregation(self):
        """Verifies that user with multiple roles inherits combined permissions."""
        RoleService.replace_roles(
            user=self.user, roles=[RoleName.SHELTER_STAFF, RoleName.VETERINARIAN]
        )

        perms = RoleService.get_permissions(self.user)
        expected_staff_perms = get_permissions_for_role(RoleName.SHELTER_STAFF)
        expected_vet_perms = get_permissions_for_role(RoleName.VETERINARIAN)

        combined_expected = expected_staff_perms | expected_vet_perms
        self.assertTrue(combined_expected.issubset(perms))

    def test_superuser_roles_and_permissions(self):
        """Verifies superuser possesses ADMINISTRATOR role and all permissions."""
        superuser_roles = RoleService.get_roles(self.actor)
        superuser_perms = RoleService.get_permissions(self.actor)

        self.assertIn(RoleName.ADMINISTRATOR, superuser_roles)
        self.assertEqual(superuser_perms, PermissionName.get_all_permissions())

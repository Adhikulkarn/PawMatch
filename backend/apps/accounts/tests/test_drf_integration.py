"""
Comprehensive test suite for Phase 1.6.4 DRF Integration & Authorization Service Optimization.
"""

from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.permissions import PermissionName
from apps.accounts.permissions_drf import (
    HasPermission,
    HasRole,
    IsAdministratorRole,
)
from apps.accounts.roles import RoleName
from apps.accounts.services.authorization_service import AuthorizationService
from apps.accounts.services.rbac_service import RBACService
from apps.accounts.services.role_service import RoleService

User = get_user_model()


class DRFIntegrationTestCase(TestCase):
    """Test suite for DRF permission integration, caching, and PolicyEngine evaluation."""

    def setUp(self):
        # Synchronize RBAC infrastructure before each test
        RBACService.sync()

        self.user = User.objects.create_user(
            email="staff@pawmatch.org",
            password="Password123!",
            first_name="Staff",
            last_name="Member",
        )
        self.admin = User.objects.create_user(
            email="admin@pawmatch.org",
            password="Password123!",
            first_name="Admin",
            last_name="User",
            is_staff=True,
            is_superuser=True,
        )

    def test_immediate_authorization_update_on_role_assignment(self):
        """Verifies that assigning a role immediately reflects in AuthorizationService checks."""
        self.assertFalse(
            AuthorizationService.has_permission(self.user, PermissionName.PETS_CREATE)
        )

        RoleService.assign_role(user=self.user, role=RoleName.SHELTER_STAFF)

        # Must immediately evaluate to True without stale cache
        self.assertTrue(
            AuthorizationService.has_permission(self.user, PermissionName.PETS_CREATE)
        )

    def test_immediate_authorization_update_on_role_removal(self):
        """Verifies that removing a role immediately revokes permissions in AuthorizationService."""
        RoleService.assign_role(user=self.user, role=RoleName.SHELTER_STAFF)
        self.assertTrue(
            AuthorizationService.has_permission(self.user, PermissionName.PETS_CREATE)
        )

        RoleService.remove_role(user=self.user, role=RoleName.SHELTER_STAFF)

        # Must immediately evaluate to False without stale cache
        self.assertFalse(
            AuthorizationService.has_permission(self.user, PermissionName.PETS_CREATE)
        )

    def test_permission_caching_and_invalidation(self):
        """Verifies request-level caching of user permissions and automatic cache invalidation."""
        RoleService.assign_role(user=self.user, role=RoleName.VOLUNTEER)

        # First resolution populates cache
        perms_1 = RoleService.get_permissions(self.user)
        self.assertTrue(hasattr(self.user, "_rbac_perms_cache"))

        # Second resolution hits cache
        perms_2 = RoleService.get_permissions(self.user)
        self.assertIs(perms_1, perms_2)

        # Role change invalidates cache
        RoleService.assign_role(user=self.user, role=RoleName.SHELTER_STAFF)
        self.assertFalse(hasattr(self.user, "_rbac_perms_cache"))

        # Re-querying fetches updated permission set
        updated_perms = RoleService.get_permissions(self.user)
        self.assertIn(PermissionName.PETS_CREATE, updated_perms)

    def test_drf_has_permission_class(self):
        """Verifies DRF HasPermission class compatibility."""
        perm_class = HasPermission(PermissionName.PETS_VIEW)
        request = SimpleNamespace(user=self.user)
        view = SimpleNamespace()

        # User without role
        self.assertFalse(perm_class.has_permission(request, view))

        # Assign role
        RoleService.assign_role(user=self.user, role=RoleName.ADOPTER)
        self.assertTrue(perm_class.has_permission(request, view))

    def test_drf_has_role_class(self):
        """Verifies DRF HasRole class compatibility."""
        role_class = HasRole(RoleName.VETERINARIAN)
        request = SimpleNamespace(user=self.user)
        view = SimpleNamespace()

        self.assertFalse(role_class.has_permission(request, view))

        RoleService.assign_role(user=self.user, role=RoleName.VETERINARIAN)
        self.assertTrue(role_class.has_permission(request, view))

    def test_drf_is_administrator_role_class(self):
        """Verifies DRF IsAdministratorRole permission class."""
        admin_class = IsAdministratorRole()
        user_request = SimpleNamespace(user=self.user)
        admin_request = SimpleNamespace(user=self.admin)
        view = SimpleNamespace()

        self.assertFalse(admin_class.has_permission(user_request, view))
        self.assertTrue(admin_class.has_permission(admin_request, view))

    def test_object_level_policy_authorization(self):
        """Verifies object-level policy authorization through AuthorizationService.can()."""
        target_pet = SimpleNamespace(_policy_type="pet", owner_id=self.user.id)

        # Owner should be allowed to update pet
        self.assertTrue(AuthorizationService.can(self.user, "can_update", target_pet))

        other_user = User.objects.create_user(
            email="other@pawmatch.org",
            password="Password123!",
            first_name="Other",
            last_name="User",
        )
        # Non-owner non-staff user should not be allowed
        self.assertFalse(AuthorizationService.can(other_user, "can_update", target_pet))

    def test_backward_compatibility(self):
        """Verifies backward compatibility for AuthorizationService helper methods."""
        RoleService.assign_role(user=self.user, role=RoleName.SHELTER_MANAGER)

        self.assertEqual(
            AuthorizationService.getUserRole(self.user), RoleName.SHELTER_MANAGER
        )
        self.assertTrue(
            AuthorizationService.has_role(self.user, RoleName.SHELTER_MANAGER)
        )
        self.assertTrue(
            AuthorizationService.has_permission(
                self.user, PermissionName.SHELTERS_MANAGE
            )
        )
        self.assertTrue(
            AuthorizationService.authorize(
                user=self.user, permission_or_action=PermissionName.SHELTERS_MANAGE
            )
        )

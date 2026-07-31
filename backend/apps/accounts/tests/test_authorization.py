"""
Comprehensive unit and integration test suite for PawMatch Authorization Framework:
Permission Registry, Role Mappings, Policy Engine, Object-Level Authorization,
AuthorizationService, DRF Permission Classes, Decorators, Events, and Audit Logs.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APITestCase

from apps.accounts.auth_decorators import require_permission, require_role
from apps.accounts.events import permission_denied_signal, permission_granted_signal
from apps.accounts.exceptions import PermissionDeniedException
from apps.accounts.permissions import PermissionName
from apps.accounts.permissions_drf import HasObjectPermission, HasPermission, HasRole
from apps.accounts.policies import PetPolicy, PolicyEngine, UserPolicy
from apps.accounts.roles import RoleName
from apps.accounts.services.authorization_service import AuthorizationService
from apps.audit_logs.models import AuditLog

User = get_user_model()


class TestAuthorizationFramework(APITestCase):
    """Test suite for PawMatch Authorization Framework."""

    def setUp(self):
        try:
            cache.clear()
        except Exception:
            pass

        self.adopter_user = User.objects.create_user(
            email="adopter@example.com",
            password="Password123!",
            first_name="Adopter",
            last_name="User",
            is_active=True,
            is_email_verified=True,
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="Password123!",
            first_name="Other",
            last_name="User",
            is_active=True,
            is_email_verified=True,
        )

        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminPassword123!",
            first_name="Admin",
            last_name="Superuser",
        )

    def tearDown(self):
        try:
            cache.clear()
        except Exception:
            pass

    def test_permission_and_role_registries(self):
        """Tests permission and role registries return valid sets of defined strings."""
        all_perms = PermissionName.get_all_permissions()
        assert PermissionName.PETS_VIEW in all_perms
        assert PermissionName.SHELTERS_MANAGE in all_perms

        all_roles = RoleName.get_all_roles()
        assert RoleName.ADMINISTRATOR in all_roles
        assert RoleName.ADOPTER in all_roles

    def test_has_permission_rbac(self):
        """Tests AuthorizationService.has_permission checks role-based permission mappings."""
        # Adopter has pets.view and pets.adopt
        assert (
            AuthorizationService.has_permission(
                self.adopter_user, PermissionName.PETS_VIEW
            )
            is True
        )
        assert (
            AuthorizationService.has_permission(
                self.adopter_user, PermissionName.PETS_ADOPT
            )
            is True
        )

        # Adopter does NOT have shelters.manage
        assert (
            AuthorizationService.has_permission(
                self.adopter_user, PermissionName.SHELTERS_MANAGE
            )
            is False
        )

        # Superuser has all permissions
        assert (
            AuthorizationService.has_permission(
                self.admin_user, PermissionName.SHELTERS_MANAGE
            )
            is True
        )

    def test_has_role(self):
        """Tests AuthorizationService.has_role identifies user roles."""
        assert (
            AuthorizationService.has_role(self.adopter_user, RoleName.ADOPTER) is True
        )
        assert (
            AuthorizationService.has_role(self.adopter_user, RoleName.ADMINISTRATOR)
            is False
        )
        assert (
            AuthorizationService.has_role(self.admin_user, RoleName.ADMINISTRATOR)
            is True
        )

    def test_policy_engine_user_policy(self):
        """Tests PolicyEngine resolves UserPolicy and evaluates object-level access rules."""
        policy = PolicyEngine.resolve_policy(self.adopter_user)
        assert isinstance(policy, UserPolicy)

        # Adopter can view their own profile object
        assert (
            PolicyEngine.evaluate(self.adopter_user, "view", self.adopter_user) is True
        )

        # Adopter CANNOT view another user's profile object
        assert (
            PolicyEngine.evaluate(self.adopter_user, "view", self.other_user) is False
        )

        # Superuser can view any profile object
        assert PolicyEngine.evaluate(self.admin_user, "view", self.other_user) is True

    def test_policy_engine_pet_policy_object_isolation(self):
        """Tests PetPolicy object-level shelter ownership and isolation rules."""
        pet_belonging_to_shelter_1 = SimpleNamespace(
            _policy_type="pet",
            shelter_id="shelter-1",
            owner_id=self.adopter_user.id,
        )

        # Adopter (owner) can update pet object
        assert (
            PolicyEngine.evaluate(
                self.adopter_user, "update", pet_belonging_to_shelter_1
            )
            is True
        )

        # Other user (non-owner) CANNOT update pet object
        assert (
            PolicyEngine.evaluate(self.other_user, "update", pet_belonging_to_shelter_1)
            is False
        )

    def test_authorization_service_authorize_success(self):
        """Tests authorize() granting permission dispatches event signal and audit record."""
        mock_handler = MagicMock()
        permission_granted_signal.connect(mock_handler)

        result = AuthorizationService.authorize(
            self.adopter_user, PermissionName.PETS_VIEW
        )
        assert result is True

        assert mock_handler.called is True
        permission_granted_signal.disconnect(mock_handler)

        audit_entry = AuditLog.objects.filter(action="AUTHORIZATION_GRANTED").first()
        assert audit_entry is not None

    def test_authorization_service_authorize_denied_raises_exception(self):
        """Tests authorize() denying permission raises PermissionDeniedException (HTTP 403) and logs audit event."""
        mock_handler = MagicMock()
        permission_denied_signal.connect(mock_handler)

        try:
            AuthorizationService.authorize(
                self.adopter_user, PermissionName.SHELTERS_MANAGE
            )
            assert False, "Should have raised PermissionDeniedException"
        except PermissionDeniedException as exc:
            assert exc.status_code == 403

        assert mock_handler.called is True
        permission_denied_signal.disconnect(mock_handler)

        audit_entry = AuditLog.objects.filter(action="AUTHORIZATION_DENIED").first()
        assert audit_entry is not None

    def test_drf_permission_classes(self):
        """Tests DRF HasPermission, HasRole, and HasObjectPermission classes."""
        request = SimpleNamespace(user=self.adopter_user)

        perm_class = HasPermission(PermissionName.PETS_VIEW)
        assert perm_class.has_permission(request, None) is True

        perm_denied_class = HasPermission(PermissionName.SHELTERS_MANAGE)
        assert perm_denied_class.has_permission(request, None) is False

        role_class = HasRole(RoleName.ADOPTER)
        assert role_class.has_permission(request, None) is True

        obj_perm_class = HasObjectPermission("update")
        assert (
            obj_perm_class.has_object_permission(request, None, self.adopter_user)
            is True
        )
        assert (
            obj_perm_class.has_object_permission(request, None, self.other_user)
            is False
        )

    def test_authorization_decorators(self):
        """Tests @require_permission and @require_role decorators."""

        @require_permission(PermissionName.PETS_VIEW)
        def view_pets_function(user=None):
            return "viewed_pets"

        assert view_pets_function(user=self.adopter_user) == "viewed_pets"

        @require_role(RoleName.ADMINISTRATOR)
        def admin_only_function(user=None):
            return "admin_action"

        try:
            admin_only_function(user=self.adopter_user)
            assert False, "Should have raised PermissionDeniedException"
        except PermissionDeniedException:
            pass

        assert admin_only_function(user=self.admin_user) == "admin_action"

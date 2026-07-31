"""
Master End-to-End (E2E) Integration Test Suite for PawMatch RBAC Module (Phase 1.6.7).
Verifies complete lifecycle across API, RoleService, RBACService, DRF Permissions, Signals, and Audit Logs.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.constants import AuditAction
from apps.accounts.events import RoleAssignedEvent, role_assigned_signal
from apps.accounts.permissions import PermissionName
from apps.accounts.roles import RoleName
from apps.accounts.services.authorization_service import AuthorizationService
from apps.accounts.services.rbac_service import RBACService
from apps.accounts.services.role_service import RoleService
from apps.audit_logs.models import AuditLog

User = get_user_model()


class RBACE2EIntegrationTestCase(APITestCase):
    """End-to-End integration test suite for the complete RBAC system lifecycle."""

    def setUp(self):
        # 1. Sync RBAC Infrastructure
        RBACService.sync()

        # 2. Create Administrator
        self.admin = User.objects.create_user(
            email="admin.e2e@pawmatch.org",
            password="Password123!",
            first_name="E2E",
            last_name="Admin",
            is_staff=True,
            is_superuser=True,
        )

        # 3. Create Target User
        self.target_user = User.objects.create_user(
            email="user.e2e@pawmatch.org",
            password="Password123!",
            first_name="Target",
            last_name="User",
        )

    def test_complete_rbac_lifecycle(self):
        """
        Executes a complete end-to-end lifecycle scenario:
        1. Query user roles (default ADOPTER).
        2. Assign SHELTER_MANAGER role via API as Administrator.
        3. Verify Event signal received and AuditLog entry recorded.
        4. Verify immediate permission expansion (shelters.manage, pets.create).
        5. Replace roles via API to VETERINARIAN.
        6. Verify immediate permission update (medical.update).
        7. Clear roles via API.
        8. Verify revocation of permissions and fallback to default.
        """
        # --- Step 1: Initial State Check ---
        self.assertIn(RoleName.ADOPTER, RoleService.get_roles(self.target_user))
        self.assertTrue(
            AuthorizationService.has_permission(
                self.target_user, PermissionName.PETS_VIEW
            )
        )
        self.assertFalse(
            AuthorizationService.has_permission(
                self.target_user, PermissionName.SHELTERS_MANAGE
            )
        )

        # --- Step 2: Assign SHELTER_MANAGER via API ---
        signal_events = []

        def handle_role_assigned(sender, event: RoleAssignedEvent, **kwargs):
            signal_events.append(event)

        role_assigned_signal.connect(handle_role_assigned)

        try:
            self.client.force_authenticate(user=self.admin)
            assign_url = reverse("rbac:assign_role", kwargs={"id": self.target_user.id})
            response = self.client.post(
                assign_url, data={"role": RoleName.SHELTER_MANAGER}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(RoleName.SHELTER_MANAGER, response.data["data"]["roles"])

            # --- Step 3: Event Signal & Audit Log Verification ---
            self.assertEqual(len(signal_events), 1)
            self.assertEqual(signal_events[0].role_name, RoleName.SHELTER_MANAGER)
            self.assertEqual(signal_events[0].assigned_by, self.admin.id)

            audit_entry = AuditLog.objects.filter(
                user_id=self.target_user.id, action=AuditAction.ROLE_ASSIGNED
            ).first()
            self.assertIsNotNone(audit_entry)
            self.assertEqual(audit_entry.details["role"], RoleName.SHELTER_MANAGER)
            self.assertEqual(audit_entry.details["assigned_by"], str(self.admin.id))

            self.target_user.refresh_from_db()
            RoleService.invalidate_user_permission_cache(self.target_user)

            # --- Step 4: Immediate Permission Expansion Check ---
            self.assertTrue(
                AuthorizationService.has_permission(
                    self.target_user, PermissionName.SHELTERS_MANAGE
                )
            )
            self.assertTrue(
                AuthorizationService.has_permission(
                    self.target_user, PermissionName.PETS_CREATE
                )
            )

            # --- Step 5: Replace Roles via API to VETERINARIAN ---
            replace_url = reverse(
                "rbac:replace_roles", kwargs={"id": self.target_user.id}
            )
            replace_resp = self.client.put(
                replace_url, data={"roles": [RoleName.VETERINARIAN]}, format="json"
            )

            self.assertEqual(replace_resp.status_code, status.HTTP_200_OK)
            self.assertEqual(
                replace_resp.data["data"]["roles"], [RoleName.VETERINARIAN]
            )

            self.target_user.refresh_from_db()
            RoleService.invalidate_user_permission_cache(self.target_user)

            # --- Step 6: Verify Permission Update ---
            self.assertTrue(
                AuthorizationService.has_permission(
                    self.target_user, PermissionName.MEDICAL_MANAGE
                )
            )
            self.assertFalse(
                AuthorizationService.has_permission(
                    self.target_user, PermissionName.SHELTERS_MANAGE
                )
            )

            # --- Step 7: Clear Roles via API ---
            clear_url = reverse("rbac:clear_roles", kwargs={"id": self.target_user.id})
            clear_resp = self.client.delete(clear_url)

            self.assertEqual(clear_resp.status_code, status.HTTP_200_OK)
            self.assertEqual(clear_resp.data["data"]["roles"], [])

            self.target_user.refresh_from_db()
            RoleService.invalidate_user_permission_cache(self.target_user)

            # --- Step 8: Verify Permission Revocation & Default Fallback ---
            self.assertFalse(
                AuthorizationService.has_permission(
                    self.target_user, PermissionName.MEDICAL_MANAGE
                )
            )
            self.assertTrue(
                AuthorizationService.has_permission(
                    self.target_user, PermissionName.PETS_VIEW
                )
            )

        finally:
            role_assigned_signal.disconnect(handle_role_assigned)

"""
Comprehensive test suite for Phase 1.6.3 RBAC REST APIs.
"""

import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.constants import AuditAction
from apps.accounts.roles import RoleName
from apps.accounts.services.rbac_service import RBACService
from apps.accounts.services.role_service import RoleService
from apps.audit_logs.models import AuditLog

User = get_user_model()


class RBACAPITestCase(APITestCase):
    """Test suite for RBAC REST APIs."""

    def setUp(self):
        # Synchronize RBAC infrastructure before each test
        RBACService.sync()

        # Admin user (Authorized to access RBAC APIs)
        self.admin_user = User.objects.create_user(
            email="admin@pawmatch.org",
            password="Password123!",
            first_name="Admin",
            last_name="User",
            is_staff=True,
            is_superuser=True,
        )

        # Standard non-admin user (Unauthorized to access RBAC APIs)
        self.standard_user = User.objects.create_user(
            email="adopter@pawmatch.org",
            password="Password123!",
            first_name="Standard",
            last_name="User",
        )

        # Target user for role assignments
        self.target_user = User.objects.create_user(
            email="target@pawmatch.org",
            password="Password123!",
            first_name="Target",
            last_name="User",
        )

    def test_list_roles_as_administrator(self):
        """Verifies Administrators can list all platform roles."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("rbac:role_list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(len(response.data["data"]), len(RoleName.get_all_roles()))

    def test_get_role_detail_as_administrator(self):
        """Verifies Administrators can retrieve single role details."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("rbac:role_detail", kwargs={"role": "SHELTER_MANAGER"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["role"], RoleName.SHELTER_MANAGER)
        self.assertEqual(response.data["data"]["display_name"], "Shelter Manager")

    def test_get_invalid_role_detail_returns_400(self):
        """Verifies requesting an invalid role detail returns 400 Bad Request."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("rbac:role_detail", kwargs={"role": "INVALID_ROLE"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

    def test_get_user_roles(self):
        """Verifies retrieving user roles via API."""
        RoleService.assign_role(user=self.target_user, role=RoleName.VOLUNTEER)
        self.client.force_authenticate(user=self.admin_user)

        url = reverse("rbac:user_roles", kwargs={"id": self.target_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(RoleName.VOLUNTEER, response.data["data"]["roles"])

    def test_get_user_permissions(self):
        """Verifies retrieving user aggregated permissions via API."""
        RoleService.assign_role(user=self.target_user, role=RoleName.VETERINARIAN)
        self.client.force_authenticate(user=self.admin_user)

        url = reverse("rbac:user_permissions", kwargs={"id": self.target_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("medical.view", response.data["data"]["permissions"])

    def test_assign_role_api_success(self):
        """Verifies assigning a role to a user via API."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("rbac:assign_role", kwargs={"id": self.target_user.id})

        response = self.client.post(url, data={"role": RoleName.SHELTER_STAFF})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(RoleName.SHELTER_STAFF, response.data["data"]["roles"])
        self.assertTrue(RoleService.has_role(self.target_user, RoleName.SHELTER_STAFF))

        # Verify audit log recorded actor
        audit = AuditLog.objects.filter(
            user_id=self.target_user.id, action=AuditAction.ROLE_ASSIGNED
        ).first()
        self.assertIsNotNone(audit)
        self.assertEqual(audit.details["assigned_by"], str(self.admin_user.id))

    def test_assign_duplicate_role_returns_400(self):
        """Verifies assigning an already possessed role returns 400 Bad Request."""
        RoleService.assign_role(user=self.target_user, role=RoleName.VOLUNTEER)
        self.client.force_authenticate(user=self.admin_user)

        url = reverse("rbac:assign_role", kwargs={"id": self.target_user.id})
        response = self.client.post(url, data={"role": RoleName.VOLUNTEER})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_role_api_success(self):
        """Verifies removing a role from a user via API."""
        RoleService.assign_role(user=self.target_user, role=RoleName.VETERINARIAN)
        self.client.force_authenticate(user=self.admin_user)

        url = reverse("rbac:remove_role", kwargs={"id": self.target_user.id})
        response = self.client.post(url, data={"role": RoleName.VETERINARIAN})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(RoleName.VETERINARIAN, response.data["data"]["roles"])

    def test_replace_roles_api_success(self):
        """Verifies replacing user roles via API."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("rbac:replace_roles", kwargs={"id": self.target_user.id})

        new_roles = [RoleName.SHELTER_MANAGER, RoleName.VETERINARIAN]
        response = self.client.put(url, data={"roles": new_roles}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(response.data["data"]["roles"]), sorted(new_roles))

    def test_clear_roles_api_success(self):
        """Verifies clearing user roles via API."""
        RoleService.assign_role(user=self.target_user, role=RoleName.VOLUNTEER)
        self.client.force_authenticate(user=self.admin_user)

        url = reverse("rbac:clear_roles", kwargs={"id": self.target_user.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["roles"], [])

    def test_non_administrator_forbidden(self):
        """Verifies non-administrators receive 403 Forbidden for RBAC APIs."""
        self.client.force_authenticate(user=self.standard_user)
        url = reverse("rbac:role_list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_unauthorized(self):
        """Verifies unauthenticated requests receive 401 Unauthorized for RBAC APIs."""
        url = reverse("rbac:role_list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nonexistent_user_returns_404(self):
        """Verifies requests for non-existent user UUID return 404 Not Found."""
        self.client.force_authenticate(user=self.admin_user)
        random_uuid = uuid.uuid4()
        url = reverse("rbac:user_roles", kwargs={"id": random_uuid})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

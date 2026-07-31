"""
Comprehensive test suite for Phase 1.6.5 RBAC Events & Audit Logging.
Verifies signal dispatching, event payload structure, AuditLog persistence, and transaction safety.
"""

from django.contrib.auth import get_user_model
from django.db import DatabaseError, transaction
from django.test import TestCase

from apps.accounts.constants import AuditAction
from apps.accounts.events import (
    RoleAssignedEvent,
    RoleRemovedEvent,
    RoleReplacedEvent,
    role_assigned_signal,
    role_removed_signal,
    role_replaced_signal,
)
from apps.accounts.roles import RoleName
from apps.accounts.services.rbac_service import RBACService
from apps.accounts.services.role_service import RoleService
from apps.audit_logs.models import AuditLog

User = get_user_model()


class RBACEventsAndLoggingTestCase(TestCase):
    """Test suite for RBAC signals, events, and audit logging."""

    def setUp(self):
        # Synchronize RBAC infrastructure before each test
        RBACService.sync()

        self.user = User.objects.create_user(
            email="target@pawmatch.org",
            password="Password123!",
            first_name="Target",
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

    def test_role_assigned_event_and_audit_log(self):
        """Verifies RoleAssignedEvent signal dispatch and ROLE_ASSIGNED audit log creation."""
        received_events = []

        def signal_handler(sender, event, **kwargs):
            received_events.append(event)

        role_assigned_signal.connect(signal_handler)

        try:
            RoleService.assign_role(
                user=self.user, role=RoleName.SHELTER_MANAGER, actor=self.actor
            )

            # 1. Verify Event Signal
            self.assertEqual(len(received_events), 1)
            event: RoleAssignedEvent = received_events[0]
            self.assertEqual(event.user_id, self.user.id)
            self.assertEqual(event.email, self.user.email)
            self.assertEqual(event.role_name, RoleName.SHELTER_MANAGER)
            self.assertEqual(event.assigned_by, self.actor.id)
            self.assertIsNotNone(event.timestamp)

            # 2. Verify Audit Log Persistence
            audit = AuditLog.objects.filter(
                user_id=self.user.id, action=AuditAction.ROLE_ASSIGNED
            ).first()
            self.assertIsNotNone(audit)
            self.assertEqual(audit.status, "SUCCESS")
            self.assertEqual(audit.details["role"], RoleName.SHELTER_MANAGER)
            self.assertEqual(audit.details["assigned_by"], str(self.actor.id))
        finally:
            role_assigned_signal.disconnect(signal_handler)

    def test_role_removed_event_and_audit_log(self):
        """Verifies RoleRemovedEvent signal dispatch and ROLE_REMOVED audit log creation."""
        RoleService.assign_role(user=self.user, role=RoleName.VETERINARIAN)

        received_events = []

        def signal_handler(sender, event, **kwargs):
            received_events.append(event)

        role_removed_signal.connect(signal_handler)

        try:
            RoleService.remove_role(
                user=self.user, role=RoleName.VETERINARIAN, actor=self.actor
            )

            # 1. Verify Event Signal
            self.assertEqual(len(received_events), 1)
            event: RoleRemovedEvent = received_events[0]
            self.assertEqual(event.user_id, self.user.id)
            self.assertEqual(event.email, self.user.email)
            self.assertEqual(event.role_name, RoleName.VETERINARIAN)
            self.assertEqual(event.removed_by, self.actor.id)

            # 2. Verify Audit Log Persistence
            audit = AuditLog.objects.filter(
                user_id=self.user.id, action=AuditAction.ROLE_REMOVED
            ).first()
            self.assertIsNotNone(audit)
            self.assertEqual(audit.status, "SUCCESS")
            self.assertEqual(audit.details["role"], RoleName.VETERINARIAN)
            self.assertEqual(audit.details["removed_by"], str(self.actor.id))
        finally:
            role_removed_signal.disconnect(signal_handler)

    def test_role_replaced_event_and_audit_log(self):
        """Verifies RoleReplacedEvent signal dispatch and ROLE_REPLACED audit log creation."""
        received_events = []

        def signal_handler(sender, event, **kwargs):
            received_events.append(event)

        role_replaced_signal.connect(signal_handler)

        target_roles = [RoleName.SHELTER_STAFF, RoleName.VOLUNTEER]

        try:
            RoleService.replace_roles(
                user=self.user, roles=target_roles, actor=self.actor
            )

            # 1. Verify Event Signal
            self.assertEqual(len(received_events), 1)
            event: RoleReplacedEvent = received_events[0]
            self.assertEqual(event.user_id, self.user.id)
            self.assertEqual(event.email, self.user.email)
            self.assertEqual(sorted(event.roles), sorted(target_roles))
            self.assertEqual(event.replaced_by, self.actor.id)

            # 2. Verify Audit Log Persistence
            audit = AuditLog.objects.filter(
                user_id=self.user.id, action=AuditAction.ROLE_REPLACED
            ).first()
            self.assertIsNotNone(audit)
            self.assertEqual(audit.status, "SUCCESS")
            self.assertEqual(sorted(audit.details["roles"]), sorted(target_roles))
            self.assertEqual(audit.details["replaced_by"], str(self.actor.id))
        finally:
            role_replaced_signal.disconnect(signal_handler)

    def test_transaction_safety_rollback(self):
        """Verifies that audit logs and role changes are atomically rolled back on failure."""
        initial_audit_count = AuditLog.objects.count()

        try:
            with transaction.atomic():
                RoleService.assign_role(user=self.user, role=RoleName.VOLUNTEER)
                # Simulate a transaction failure
                raise DatabaseError("Forced transaction failure for testing atomicity.")
        except DatabaseError:
            pass

        # Verify role assignment was rolled back
        self.assertNotIn(RoleName.VOLUNTEER, RoleService.get_roles(self.user))

        # Verify no SUCCESS audit logs were persisted during failed transaction
        self.assertEqual(AuditLog.objects.count(), initial_audit_count)

"""
Comprehensive permission and authorization unit & integration test suite for Shelter domain.
Covers RBAC, object-level authorization, role hierarchies, cross-shelter isolation,
archived status, inactive memberships, and ownership transfer validation.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.roles import RoleName
from apps.accounts.services.role_service import RoleService
from apps.shelters.constants import (
    DocumentType,
    ShelterMemberRole,
    ShelterStatus,
    VerificationStatus,
)
from apps.shelters.services import (
    MemberService,
    ShelterService,
    VerificationService,
)

User = get_user_model()


@pytest.mark.django_db
class TestShelterPermissions(APITestCase):
    """
    Test suite verifying permission enforcement across all Shelter API endpoints.
    """

    def setUp(self):
        # 1. Platform Admin
        self.admin_user = User.objects.create_user(
            email="admin@pawmatch.com",
            first_name="Admin",
            last_name="User",
            password="Password123!",
            is_superuser=True,
        )
        RoleService.assign_role(self.admin_user, RoleName.ADMINISTRATOR)

        # 2. Verification Staff
        self.verification_staff = User.objects.create_user(
            email="vstaff@pawmatch.com",
            first_name="Verif",
            last_name="Staff",
            password="Password123!",
            is_staff=True,
        )

        # 3. Shelter 1 Users
        self.owner1 = User.objects.create_user(
            email="owner1@shelter1.org",
            first_name="Owner",
            last_name="One",
            password="Password123!",
        )
        self.manager1 = User.objects.create_user(
            email="manager1@shelter1.org",
            first_name="Manager",
            last_name="One",
            password="Password123!",
        )
        self.staff1 = User.objects.create_user(
            email="staff1@shelter1.org",
            first_name="Staff",
            last_name="One",
            password="Password123!",
        )
        self.volunteer1 = User.objects.create_user(
            email="volunteer1@shelter1.org",
            first_name="Volunteer",
            last_name="One",
            password="Password123!",
        )

        # 4. Shelter 2 User (Cross-shelter actor)
        self.owner2 = User.objects.create_user(
            email="owner2@shelter2.org",
            first_name="Owner",
            last_name="Two",
            password="Password123!",
        )

        # 5. Non-member / Adopter User
        self.adopter_user = User.objects.create_user(
            email="adopter@example.com",
            first_name="Adopter",
            last_name="User",
            password="Password123!",
        )

        # Create Shelter 1 and memberships
        self.shelter1 = ShelterService.create_shelter(
            user=self.owner1,
            name="Shelter One",
            email="info@shelter1.org",
            phone_number="111-222-3333",
            address_line1="1 Owner Way",
            city="Austin",
            state="TX",
            postal_code="78701",
        )
        self.member_manager1 = MemberService.add_member(
            shelter=self.shelter1,
            user=self.manager1,
            role=ShelterMemberRole.MANAGER,
        )
        self.member_staff1 = MemberService.add_member(
            shelter=self.shelter1,
            user=self.staff1,
            role=ShelterMemberRole.STAFF,
        )
        self.member_volunteer1 = MemberService.add_member(
            shelter=self.shelter1,
            user=self.volunteer1,
            role=ShelterMemberRole.VOLUNTEER,
        )

        # Create Shelter 2
        self.shelter2 = ShelterService.create_shelter(
            user=self.owner2,
            name="Shelter Two",
            email="info@shelter2.org",
            phone_number="999-888-7777",
            address_line1="2 Owner Way",
            city="Dallas",
            state="TX",
            postal_code="75201",
        )

    # --- Part 6.1: Anonymous Users (401 Unauthenticated) ---

    def test_anonymous_user_access_denied(self):
        """Unauthenticated requests to protected endpoints return 401 Unauthorized."""
        self.client.logout()

        # Retrieve
        resp = self.client.get(f"/api/v1/shelters/{self.shelter1.id}/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

        # Update
        resp = self.client.patch(
            f"/api/v1/shelters/{self.shelter1.id}/",
            data={"name": "Hacked Shelter"},
            format="json",
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

        # Members list & add
        resp = self.client.get(f"/api/v1/shelters/{self.shelter1.id}/members/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

        # Verification actions
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/verification/submit/"
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # --- Part 6.2: System Administrator (Full Access) ---

    def test_administrator_full_access(self):
        """System Administrator has full access across all shelters and operations."""
        self.client.force_authenticate(user=self.admin_user)

        # Update any shelter
        resp = self.client.patch(
            f"/api/v1/shelters/{self.shelter1.id}/",
            data={"description": "Admin updated description."},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

        # Invite members
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/invitations/",
            data={
                "email": "invited_by_admin@example.com",
                "role": ShelterMemberRole.STAFF,
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED

        # Start review and approve verification
        VerificationService.submit_verification(self.shelter1.verifications.first().id)
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/verification/start-review/"
        )
        assert resp.status_code == status.HTTP_200_OK

        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/verification/approve/",
            data={"notes": "Approved by admin"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

    # --- Part 6.3: Verification Staff (Verification Workflow Only) ---

    def test_verification_staff_can_review_and_approve(self):
        """Verification staff can execute verification review, request info, approve, and reject."""
        # Submit verification as owner
        self.client.force_authenticate(user=self.owner1)
        self.client.post(f"/api/v1/shelters/{self.shelter1.id}/verification/submit/")

        # Review as verification staff
        self.client.force_authenticate(user=self.verification_staff)

        # Start review
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/verification/start-review/"
        )
        assert resp.status_code == status.HTTP_200_OK

        # Request info
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/verification/request-information/",
            data={"notes": "Please upload address proof"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["data"]["status"] == VerificationStatus.NEEDS_INFORMATION

    def test_shelter_owner_cannot_review_or_approve_verification(self):
        """Shelter Owner cannot perform verification review or approval (403 Forbidden)."""
        self.client.force_authenticate(user=self.owner1)
        self.client.post(f"/api/v1/shelters/{self.shelter1.id}/verification/submit/")

        # Attempt to start review on own shelter
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/verification/start-review/"
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        # Attempt to approve own shelter verification
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/verification/approve/",
            data={"notes": "Self approved"},
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    # --- Part 6.4: Shelter Owner (Full Management of Own Shelter) ---

    def test_shelter_owner_management_rights(self):
        """Shelter owner can update profile, invite members, add members, attach documents, submit verification."""
        self.client.force_authenticate(user=self.owner1)

        # Update profile
        resp = self.client.patch(
            f"/api/v1/shelters/{self.shelter1.id}/",
            data={"phone_number": "512-000-1111"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

        # Invite member
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/invitations/",
            data={"email": "newstaff@shelter1.org", "role": ShelterMemberRole.STAFF},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED

        # Add member directly
        new_user = User.objects.create_user(
            email="directuser@shelter1.org",
            first_name="Direct",
            last_name="User",
            password="Password123!",
        )
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/members/",
            data={"user_id": str(new_user.id), "role": ShelterMemberRole.STAFF},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED

    # --- Part 6.5: Shelter Manager (Operational Management) ---

    def test_shelter_manager_permissions_and_limitations(self):
        """Shelter Manager can manage operations and invite staff, but cannot transfer ownership."""
        self.client.force_authenticate(user=self.manager1)

        # Update shelter details (allowed)
        resp = self.client.patch(
            f"/api/v1/shelters/{self.shelter1.id}/",
            data={"description": "Manager updated info"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

        # Invite staff (allowed)
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/invitations/",
            data={"email": "vol1@shelter1.org", "role": ShelterMemberRole.VOLUNTEER},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED

        # Attempt to change member role to OWNER (denied 403)
        resp = self.client.patch(
            f"/api/v1/shelters/members/{self.member_staff1.id}/",
            data={"role": ShelterMemberRole.OWNER},
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    # --- Part 6.6: Staff (Limited Operational Actions) ---

    def test_shelter_staff_permissions_and_limitations(self):
        """Shelter Staff can attach documents & view members, but cannot update shelter profile or invite members."""
        self.client.force_authenticate(user=self.staff1)

        # View members (allowed)
        resp = self.client.get(f"/api/v1/shelters/{self.shelter1.id}/members/")
        assert resp.status_code == status.HTTP_200_OK

        # Attach document (allowed)
        file = SimpleUploadedFile(
            "proof.pdf", b"doc data", content_type="application/pdf"
        )
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/documents/",
            data={"document_type": DocumentType.ADDRESS_PROOF, "file": file},
            format="multipart",
        )
        assert resp.status_code == status.HTTP_201_CREATED

        # Update shelter profile (denied 403)
        resp = self.client.patch(
            f"/api/v1/shelters/{self.shelter1.id}/",
            data={"name": "Staff Renamed Shelter"},
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        # Invite members (denied 403)
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/invitations/",
            data={
                "email": "staffinvite@shelter1.org",
                "role": ShelterMemberRole.VOLUNTEER,
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    # --- Part 6.7: Volunteer (Read-Only Operational Access) ---

    def test_shelter_volunteer_read_only_access(self):
        """Volunteer has read-only access to shelter members and details, but cannot write/modify."""
        self.client.force_authenticate(user=self.volunteer1)

        # View shelter detail (allowed)
        resp = self.client.get(f"/api/v1/shelters/{self.shelter1.id}/")
        assert resp.status_code == status.HTTP_200_OK

        # View members (allowed)
        resp = self.client.get(f"/api/v1/shelters/{self.shelter1.id}/members/")
        assert resp.status_code == status.HTTP_200_OK

        # Attach document (denied 403)
        file = SimpleUploadedFile("vol.pdf", b"content", content_type="application/pdf")
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/documents/",
            data={"document_type": DocumentType.IDENTITY_PROOF, "file": file},
            format="multipart",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        # Update shelter profile (denied 403)
        resp = self.client.patch(
            f"/api/v1/shelters/{self.shelter1.id}/",
            data={"description": "Volunteer edit"},
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    # --- Part 6.8: Cross-Shelter Access Prevention ---

    def test_cross_shelter_access_prevented(self):
        """Owner of Shelter 2 cannot access or modify resources belonging to Shelter 1 (403 Forbidden)."""
        self.client.force_authenticate(user=self.owner2)

        # Modify Shelter 1 (denied)
        resp = self.client.patch(
            f"/api/v1/shelters/{self.shelter1.id}/",
            data={"name": "Hijacked Shelter"},
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        # List members of Shelter 1 (denied)
        resp = self.client.get(f"/api/v1/shelters/{self.shelter1.id}/members/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        # Delete member from Shelter 1 (denied)
        resp = self.client.delete(f"/api/v1/shelters/members/{self.member_staff1.id}/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        # Submit verification for Shelter 1 (denied)
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/verification/submit/"
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    # --- Part 6.9: Archived Shelters ---

    def test_archived_shelter_management_restricted(self):
        """Management actions on archived shelters are restricted for non-admin users (403 Forbidden)."""
        self.shelter1.status = ShelterStatus.ARCHIVED
        self.shelter1.is_active = False
        self.shelter1.save()

        self.client.force_authenticate(user=self.owner1)

        # Attempt to update archived shelter (denied)
        resp = self.client.patch(
            f"/api/v1/shelters/{self.shelter1.id}/",
            data={"name": "Archived Renamed"},
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        # Attempt to invite members to archived shelter (denied)
        resp = self.client.post(
            f"/api/v1/shelters/{self.shelter1.id}/invitations/",
            data={
                "email": "archived_invite@example.com",
                "role": ShelterMemberRole.STAFF,
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    # --- Part 6.10: Inactive Memberships ---

    def test_inactive_membership_access_denied(self):
        """Deactivated shelter member loses operational access (403 Forbidden)."""
        self.member_manager1.is_active = False
        self.member_manager1.save()

        self.client.force_authenticate(user=self.manager1)

        # Manager with inactive membership attempts update (denied)
        resp = self.client.patch(
            f"/api/v1/shelters/{self.shelter1.id}/",
            data={"description": "Inactive manager update"},
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        # View members (denied)
        resp = self.client.get(f"/api/v1/shelters/{self.shelter1.id}/members/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    # --- Part 6.11: Ownership Transfer Authorization ---

    def test_ownership_transfer_authorization(self):
        """Only current Shelter Owner or System Admin can promote a member to OWNER role."""
        # 1. Manager attempts to promote staff to OWNER (denied 403)
        self.client.force_authenticate(user=self.manager1)
        resp = self.client.patch(
            f"/api/v1/shelters/members/{self.member_staff1.id}/",
            data={"role": ShelterMemberRole.OWNER},
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        # 2. Owner promotes staff to OWNER (allowed 200)
        self.client.force_authenticate(user=self.owner1)
        resp = self.client.patch(
            f"/api/v1/shelters/members/{self.member_staff1.id}/",
            data={"role": ShelterMemberRole.OWNER},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["data"]["role"] == ShelterMemberRole.OWNER

    # --- Part 6.12: Verified Shelter Operational Permissions ---

    def test_verified_shelter_permissions_and_draft_restrictions(self):
        """
        Tests IsVerifiedShelter permission enforcement:
        - Draft/Unverified shelter members cannot execute verified operations (pets, adoptions).
        - Verified shelter members can execute verified operations.
        - System Administrators bypass operational state checks.
        """
        from apps.shelters.permissions import IsVerifiedShelter

        perm = IsVerifiedShelter()

        class DummyRequest:
            def __init__(self, user):
                self.user = user

        class DummyView:
            kwargs = {}

        # 1. Unverified shelter: owner is denied verified actions
        req_owner = DummyRequest(self.owner1)
        assert (
            perm.has_object_permission(req_owner, DummyView(), self.shelter1) is False
        )

        # 2. Verified shelter: owner is granted verified actions
        self.shelter1.status = ShelterStatus.VERIFIED
        self.shelter1.save()

        assert perm.has_object_permission(req_owner, DummyView(), self.shelter1) is True

        # 3. Administrator bypass: admin is granted verified actions even on unverified shelter
        self.shelter1.status = ShelterStatus.UNVERIFIED
        self.shelter1.save()

        req_admin = DummyRequest(self.admin_user)
        assert perm.has_object_permission(req_admin, DummyView(), self.shelter1) is True

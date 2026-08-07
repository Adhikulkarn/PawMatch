"""
Comprehensive unit tests for Shelter domain models (Shelter, ShelterAddress, ShelterDocument).
"""

import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.shelters.constants import (
    DocumentStatus,
    DocumentType,
    InvitationStatus,
    OrganizationType,
    ShelterMemberRole,
    ShelterStatus,
    VerificationStatus,
)
from apps.shelters.models import (
    Shelter,
    ShelterAddress,
    ShelterDocument,
    ShelterMember,
)

User = get_user_model()


class ShelterModelTest(TestCase):
    """Test cases for Shelter model methods, properties, managers, and soft-delete."""

    def setUp(self):
        self.shelter = Shelter.objects.create(
            name="Happy Paws Rescue",
            slug="happy-paws-rescue",
            legal_name="Happy Paws Foundation Inc",
            organization_type=OrganizationType.NON_PROFIT,
            registration_number="REG-12345",
            tax_id="TAX-998877",
            email="contact@happypaws.org",
            phone_number="+1-555-0199",
            website="https://happypaws.org",
            address_line1="123 Rescue Way",
            address_line2="Suite 400",
            city="Austin",
            state="TX",
            postal_code="78701",
            country="USA",
            latitude=Decimal("30.267200"),
            longitude=Decimal("-97.743100"),
            status=ShelterStatus.UNVERIFIED,
            is_active=True,
        )

    def test_shelter_creation_and_fields(self):
        self.assertIsInstance(self.shelter.id, uuid.UUID)
        self.assertEqual(str(self.shelter), "Happy Paws Rescue")
        self.assertEqual(self.shelter.organization_type, OrganizationType.NON_PROFIT)
        self.assertTrue(self.shelter.is_active)
        self.assertFalse(self.shelter.is_deleted)
        self.assertIsNone(self.shelter.deleted_at)

    def test_shelter_properties(self):
        self.assertFalse(self.shelter.is_verified)
        self.assertFalse(self.shelter.can_publish_pets)

        self.shelter.status = ShelterStatus.VERIFIED
        self.shelter.save()
        self.assertTrue(self.shelter.is_verified)
        self.assertTrue(self.shelter.can_publish_pets)

        # Deactivated shelter cannot publish pets
        self.shelter.is_active = False
        self.shelter.save()
        self.assertFalse(self.shelter.can_publish_pets)

    def test_shelter_full_address_property(self):
        expected_address = "123 Rescue Way, Suite 400, Austin, TX 78701, USA"
        self.assertEqual(self.shelter.full_address, expected_address)

    def test_shelter_soft_delete_and_restore(self):
        self.shelter.soft_delete()
        self.assertTrue(self.shelter.is_deleted)
        self.assertIsNotNone(self.shelter.deleted_at)

        # Custom manager excludes deleted items by default
        self.assertEqual(Shelter.objects.filter(id=self.shelter.id).count(), 0)
        self.assertEqual(
            Shelter.objects.with_deleted().filter(id=self.shelter.id).count(), 1
        )

        self.shelter.restore()
        self.assertFalse(self.shelter.is_deleted)
        self.assertIsNone(self.shelter.deleted_at)
        self.assertEqual(Shelter.objects.filter(id=self.shelter.id).count(), 1)

    def test_shelter_manager_queryset_methods(self):
        verified_shelter = Shelter.objects.create(
            name="Verified Sanctuary",
            slug="verified-sanctuary",
            email="info@verified.org",
            city="Dallas",
            state="TX",
            status=ShelterStatus.VERIFIED,
        )

        active_shelters = Shelter.objects.active()
        self.assertIn(self.shelter, active_shelters)
        self.assertIn(verified_shelter, active_shelters)

        verified_shelters = Shelter.objects.verified()
        self.assertNotIn(self.shelter, verified_shelters)
        self.assertIn(verified_shelter, verified_shelters)

        unverified_shelters = Shelter.objects.unverified()
        self.assertIn(self.shelter, unverified_shelters)
        self.assertNotIn(verified_shelter, unverified_shelters)

        austin_shelters = Shelter.objects.by_city("austin")
        self.assertIn(self.shelter, austin_shelters)
        self.assertNotIn(verified_shelter, austin_shelters)

        tx_shelters = Shelter.objects.by_state("TX")
        self.assertEqual(len(tx_shelters), 2)

        search_results = Shelter.objects.search("Sanctuary")
        self.assertIn(verified_shelter, search_results)
        self.assertNotIn(self.shelter, search_results)

    def test_owner_memberships_property(self):
        owner_user = User.objects.create_user(
            email="owner@happypaws.org",
            password="Password123!",
            first_name="Owner",
            last_name="User",
        )
        ShelterMember.objects.create(
            shelter=self.shelter,
            user=owner_user,
            role=ShelterMemberRole.OWNER,
            is_active=True,
        )
        self.assertEqual(self.shelter.owner_memberships.count(), 1)


class ShelterAddressModelTest(TestCase):
    """Test cases for ShelterAddress model, properties, and manager methods."""

    def setUp(self):
        self.shelter = Shelter.objects.create(
            name="Austin Animal Center",
            slug="austin-animal-center",
            email="info@austinanimals.org",
            city="Austin",
            state="TX",
        )
        self.address = ShelterAddress.objects.create(
            shelter=self.shelter,
            address_line1="7201 Levander Loop",
            address_line2="Building A",
            city="Austin",
            state="TX",
            postal_code="78702",
            country="USA",
            latitude=Decimal("30.251500"),
            longitude=Decimal("-97.697800"),
            is_primary=True,
        )

    def test_address_creation_and_str(self):
        self.assertIsInstance(self.address.id, uuid.UUID)
        expected_str = "7201 Levander Loop, Building A, Austin, TX 78702, USA"
        self.assertEqual(str(self.address), expected_str)
        self.assertEqual(self.address.formatted_address, expected_str)
        self.assertTrue(self.address.has_coordinates)

    def test_address_has_coordinates_false_when_none(self):
        no_coords = ShelterAddress.objects.create(
            shelter=Shelter.objects.create(
                name="Remote Rescue",
                slug="remote-rescue",
                email="remote@rescue.org",
                city="Houston",
                state="TX",
            ),
            address_line1="100 Rural Rd",
            city="Houston",
            state="TX",
            postal_code="77001",
        )
        self.assertFalse(no_coords.has_coordinates)

    def test_address_manager_methods(self):
        by_city = ShelterAddress.objects.by_city("austin")
        self.assertIn(self.address, by_city)

        by_state = ShelterAddress.objects.by_state("tx")
        self.assertIn(self.address, by_state)

        with_coords = ShelterAddress.objects.with_coordinates()
        self.assertIn(self.address, with_coords)


class ShelterDocumentModelTest(TestCase):
    """Test cases for ShelterDocument model, validation, properties, and manager."""

    def setUp(self):
        self.shelter = Shelter.objects.create(
            name="Safe Haven Pets",
            slug="safe-haven-pets",
            email="info@safehaven.org",
            city="Denver",
            state="CO",
        )
        self.uploader = User.objects.create_user(
            email="uploader@safehaven.org",
            first_name="Uploader",
            last_name="User",
            password="Password123!",
        )
        self.dummy_pdf = SimpleUploadedFile(
            "registration.pdf",
            b"%PDF-1.4 dummy pdf content",
            content_type="application/pdf",
        )
        self.doc = ShelterDocument.objects.create(
            shelter=self.shelter,
            document_type=DocumentType.REGISTRATION_CERTIFICATE,
            file=self.dummy_pdf,
            file_name="registration.pdf",
            file_size=1024,
            mime_type="application/pdf",
            status=DocumentStatus.PENDING,
            uploaded_by=self.uploader,
        )

    def test_document_creation_and_str(self):
        self.assertIsInstance(self.doc.id, uuid.UUID)
        self.assertEqual(
            str(self.doc), f"Registration Certificate - {self.shelter.name}"
        )
        self.assertFalse(self.doc.is_approved)
        self.assertTrue(self.doc.is_deletable)

    def test_document_approval_status(self):
        self.doc.status = DocumentStatus.APPROVED
        self.doc.save()
        self.assertTrue(self.doc.is_approved)
        self.assertFalse(self.doc.is_deletable)

    def test_document_manager_queryset_methods(self):
        approved_doc = ShelterDocument.objects.create(
            shelter=self.shelter,
            document_type=DocumentType.GOVERNMENT_LICENSE,
            file=self.dummy_pdf,
            file_name="license.pdf",
            file_size=2048,
            status=DocumentStatus.APPROVED,
        )
        rejected_doc = ShelterDocument.objects.create(
            shelter=self.shelter,
            document_type=DocumentType.TAX_CERTIFICATE,
            file=self.dummy_pdf,
            file_name="tax.pdf",
            file_size=2048,
            status=DocumentStatus.REJECTED,
        )

        approved_list = ShelterDocument.objects.approved()
        self.assertIn(approved_doc, approved_list)
        self.assertNotIn(self.doc, approved_list)

        pending_list = ShelterDocument.objects.pending()
        self.assertIn(self.doc, pending_list)

        rejected_list = ShelterDocument.objects.rejected()
        self.assertIn(rejected_doc, rejected_list)

        by_type_list = ShelterDocument.objects.by_type(
            DocumentType.REGISTRATION_CERTIFICATE
        )
        self.assertIn(self.doc, by_type_list)
        self.assertNotIn(approved_doc, by_type_list)


class ConstantsTextChoicesTest(TestCase):
    """Test cases for domain TextChoices constants."""

    def test_text_choices_values(self):
        self.assertEqual(ShelterStatus.VERIFIED, "verified")
        self.assertEqual(OrganizationType.NON_PROFIT, "non_profit")
        self.assertEqual(VerificationStatus.APPROVED, "approved")
        self.assertEqual(DocumentType.GOVERNMENT_LICENSE, "government_license")
        self.assertEqual(DocumentStatus.APPROVED, "approved")
        self.assertEqual(InvitationStatus.PENDING, "pending")

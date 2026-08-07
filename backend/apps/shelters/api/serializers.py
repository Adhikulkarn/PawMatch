"""
DRF Serializers for Shelter domain entities, validation, and request payloads.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.shelters.constants import (
    DEFAULT_INVITATION_EXPIRY_DAYS,
    DocumentType,
    ShelterMemberRole,
)
from apps.shelters.models import (
    Shelter,
    ShelterDocument,
    ShelterInvitation,
    ShelterMember,
    ShelterVerification,
)
from apps.shelters.validators import (
    validate_document_file_size,
    validate_document_mime_type,
)

User = get_user_model()


# --- Shelter Serializers ---


class ShelterListSerializer(serializers.ModelSerializer):
    """Compact serializer for shelter catalog listings."""

    is_verified = serializers.BooleanField(read_only=True)
    can_publish_pets = serializers.BooleanField(read_only=True)

    class Meta:
        model = Shelter
        fields = [
            "id",
            "name",
            "slug",
            "city",
            "state",
            "country",
            "status",
            "is_verified",
            "can_publish_pets",
            "logo",
            "created_at",
        ]
        read_only_fields = fields


class ShelterDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for full shelter profile views."""

    is_verified = serializers.BooleanField(read_only=True)
    can_publish_pets = serializers.BooleanField(read_only=True)

    class Meta:
        model = Shelter
        fields = [
            "id",
            "name",
            "slug",
            "legal_name",
            "registration_number",
            "tax_id",
            "email",
            "phone_number",
            "website",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "description",
            "logo",
            "banner_image",
            "status",
            "is_verified",
            "can_publish_pets",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "status",
            "is_verified",
            "can_publish_pets",
            "created_at",
            "updated_at",
        ]


class ShelterCreateSerializer(serializers.ModelSerializer):
    """Request payload serializer for onboarding a new shelter."""

    email = serializers.EmailField()

    class Meta:
        model = Shelter
        fields = [
            "name",
            "legal_name",
            "registration_number",
            "tax_id",
            "email",
            "phone_number",
            "website",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "description",
            "logo",
            "banner_image",
        ]

    def validate_name(self, value: str) -> str:
        name = value.strip()
        if len(name) < 2:
            raise serializers.ValidationError(
                "Shelter name must be at least 2 characters."
            )
        return name


ShelterRegisterSerializer = ShelterCreateSerializer


class ShelterUpdateSerializer(serializers.ModelSerializer):
    """Request payload serializer for updating shelter profile details."""

    class Meta:
        model = Shelter
        fields = [
            "name",
            "legal_name",
            "registration_number",
            "tax_id",
            "email",
            "phone_number",
            "website",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "description",
            "logo",
            "banner_image",
        ]
        extra_kwargs = {field: {"required": False} for field in fields}


# --- Member Serializers ---


class ShelterMemberUserSerializer(serializers.ModelSerializer):
    """Nested user representation in member endpoints."""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
        read_only_fields = fields


class ShelterMemberSerializer(serializers.ModelSerializer):
    """Serializer for ShelterMember records."""

    user = ShelterMemberUserSerializer(read_only=True)
    is_owner = serializers.BooleanField(read_only=True)
    is_manager = serializers.BooleanField(read_only=True)

    class Meta:
        model = ShelterMember
        fields = [
            "id",
            "shelter",
            "user",
            "role",
            "is_active",
            "is_owner",
            "is_manager",
            "joined_at",
            "created_at",
        ]
        read_only_fields = fields


class MemberAddSerializer(serializers.Serializer):
    """Request payload for adding a member directly."""

    user_id = serializers.UUIDField()
    role = serializers.ChoiceField(
        choices=ShelterMemberRole.choices, default=ShelterMemberRole.VOLUNTEER
    )


class MemberUpdateSerializer(serializers.Serializer):
    """Request payload for updating a member's role."""

    role = serializers.ChoiceField(choices=ShelterMemberRole.choices)


class OwnershipTransferSerializer(serializers.Serializer):
    """Request payload for transferring shelter ownership."""

    new_owner_user_id = serializers.UUIDField(required=True)


# --- Verification Serializers ---


class ShelterVerificationSerializer(serializers.ModelSerializer):
    """Serializer for ShelterVerification workflow state."""

    reviewed_by = ShelterMemberUserSerializer(read_only=True)
    is_active_workflow = serializers.BooleanField(read_only=True)

    class Meta:
        model = ShelterVerification
        fields = [
            "id",
            "shelter",
            "status",
            "reviewer_notes",
            "rejection_reason",
            "submitted_at",
            "reviewed_at",
            "reviewed_by",
            "is_active_workflow",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class VerificationRequestInfoSerializer(serializers.Serializer):
    """Request payload for requesting info during verification review."""

    notes = serializers.CharField(required=True, min_length=5)


class VerificationApproveSerializer(serializers.Serializer):
    """Request payload for approving a verification request."""

    notes = serializers.CharField(required=False, allow_blank=True, default="")


class VerificationRejectSerializer(serializers.Serializer):
    """Request payload for rejecting a verification request."""

    reason = serializers.CharField(required=True, min_length=5)


# --- Document Serializers ---


class ShelterDocumentSerializer(serializers.ModelSerializer):
    """Serializer for ShelterDocument entity."""

    uploaded_by = ShelterMemberUserSerializer(read_only=True)
    verified_by = ShelterMemberUserSerializer(read_only=True)
    is_deletable = serializers.BooleanField(read_only=True)

    class Meta:
        model = ShelterDocument
        fields = [
            "id",
            "shelter",
            "verification",
            "document_type",
            "file",
            "file_name",
            "file_size",
            "mime_type",
            "status",
            "uploaded_by",
            "verified_by",
            "is_deletable",
            "created_at",
        ]
        read_only_fields = fields


class DocumentAttachSerializer(serializers.Serializer):
    """Request payload for uploading a shelter verification document."""

    document_type = serializers.ChoiceField(choices=DocumentType.choices)
    file = serializers.FileField(
        validators=[validate_document_file_size, validate_document_mime_type]
    )


# --- Invitation Serializers ---


class ShelterInvitationSerializer(serializers.ModelSerializer):
    """Serializer for ShelterInvitation entity."""

    invited_by = ShelterMemberUserSerializer(read_only=True)
    accepted_by = ShelterMemberUserSerializer(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = ShelterInvitation
        fields = [
            "id",
            "shelter",
            "email",
            "role",
            "token",
            "status",
            "invited_by",
            "accepted_by",
            "expires_at",
            "responded_at",
            "accepted_at",
            "is_expired",
            "is_valid",
            "created_at",
        ]
        read_only_fields = fields


class InvitationCreateSerializer(serializers.Serializer):
    """Request payload for creating a staff/volunteer invitation."""

    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=ShelterMemberRole.choices, default=ShelterMemberRole.VOLUNTEER
    )
    expiry_days = serializers.IntegerField(
        default=DEFAULT_INVITATION_EXPIRY_DAYS, min_value=1, max_value=30
    )


class InvitationAcceptSerializer(serializers.Serializer):
    """Request payload for accepting an invitation token."""

    token = serializers.CharField(required=True)


class InvitationRevokeSerializer(serializers.Serializer):
    """Request payload for revoking an invitation."""

    invitation_id = serializers.UUIDField(required=True)


class ShelterDashboardSerializer(serializers.Serializer):
    """Response serializer for GET /api/v1/shelters/dashboard/."""

    organization_name = serializers.CharField()
    verification_status = serializers.CharField()
    total_pets = serializers.IntegerField(default=0)
    available_pets = serializers.IntegerField(default=0)
    adopted_pets = serializers.IntegerField(default=0)
    pending_applications = serializers.IntegerField(default=0)
    recent_notifications = serializers.ListField(
        child=serializers.DictField(), default=list
    )
    is_verified = serializers.BooleanField(default=False)
    can_publish_pets = serializers.BooleanField(default=False)

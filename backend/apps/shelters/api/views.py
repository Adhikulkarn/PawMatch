"""
Django REST Framework API Views & ViewSets for Shelter domain management.
"""

import functools
import uuid
from typing import Any

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.pagination import StandardResultsSetPagination
from apps.core.responses import api_response
from apps.shelters.api.serializers import (
    DocumentAttachSerializer,
    InvitationAcceptSerializer,
    InvitationCreateSerializer,
    InvitationRevokeSerializer,
    MemberAddSerializer,
    MemberUpdateSerializer,
    ShelterCreateSerializer,
    ShelterDetailSerializer,
    ShelterDocumentSerializer,
    ShelterInvitationSerializer,
    ShelterListSerializer,
    ShelterMemberSerializer,
    ShelterUpdateSerializer,
    ShelterVerificationSerializer,
    VerificationApproveSerializer,
    VerificationRejectSerializer,
    VerificationRequestInfoSerializer,
)
from apps.shelters.exceptions import (
    DocumentProtectedException,
    InvitationExpiredException,
    LastOwnerRemovalException,
    MemberAlreadyExistsException,
    ShelterDomainException,
    ShelterNotFoundException,
    VerificationWorkflowException,
)
from apps.shelters.models import Shelter
from apps.shelters.permissions import (
    CanDeleteDocument,
    CanInviteMembers,
    CanManageMember,
    CanManageShelter,
    CanReviewVerification,
    CanRevokeInvitation,
    CanViewShelter,
    IsShelterManager,
    IsShelterMember,
    IsShelterStaff,
)
from apps.shelters.selectors import (
    get_active_verification,
    get_shelter_by_id,
    get_shelter_members,
    list_shelter_documents,
    list_shelter_invitations,
)
from apps.shelters.services import (
    InvitationService,
    MemberService,
    ShelterService,
    VerificationService,
)

User = get_user_model()


def _parse_uuid(val: Any) -> uuid.UUID:
    """Safely convert a string or UUID object to a UUID instance."""
    if isinstance(val, uuid.UUID):
        return val
    try:
        return uuid.UUID(str(val))
    except (ValueError, TypeError, AttributeError):
        raise NotFound("Invalid UUID format.")


def handle_domain_exceptions(func):
    """Decorator mapping shelter domain exceptions into standardized API error responses."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ShelterNotFoundException as e:
            return api_response(
                success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND
            )
        except MemberAlreadyExistsException as e:
            return api_response(
                success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )
        except (
            VerificationWorkflowException,
            DocumentProtectedException,
            LastOwnerRemovalException,
            InvitationExpiredException,
            ShelterDomainException,
        ) as e:
            return api_response(
                success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )

    return wrapper


@extend_schema_view(
    list=extend_schema(
        summary="List Shelters",
        description="Returns a paginated list of shelters with searching and filtering.",
        responses={200: ShelterListSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Create Shelter",
        description="Onboards a new shelter organization and initializes owner membership and draft verification.",
        request=ShelterCreateSerializer,
        responses={201: ShelterDetailSerializer},
    ),
    retrieve=extend_schema(
        summary="Retrieve Shelter",
        description="Fetches detailed shelter organization profile by UUID.",
        responses={200: ShelterDetailSerializer, 404: None},
    ),
    partial_update=extend_schema(
        summary="Update Shelter Profile",
        description="Updates shelter profile details.",
        request=ShelterUpdateSerializer,
        responses={200: ShelterDetailSerializer},
    ),
)
class ShelterViewSet(viewsets.GenericViewSet):
    """ViewSet for Shelter organization catalog, creation, and verification workflows."""

    queryset = Shelter.objects.filter(is_deleted=False)
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "city", "state", "is_active"]
    search_fields = ["name", "legal_name", "city", "state"]
    ordering_fields = ["created_at", "name", "status"]
    ordering = ["-created_at"]

    def get_permissions(self):
        """Dynamic permission class mapping per endpoint action."""
        if self.action in ["list", "create"]:
            return [IsAuthenticated()]
        if self.action == "retrieve":
            return [IsAuthenticated(), CanViewShelter()]
        if self.action == "partial_update":
            return [IsAuthenticated(), CanManageShelter()]
        if self.action == "submit_verification":
            return [IsAuthenticated(), CanManageShelter()]
        if self.action in [
            "start_review",
            "request_information",
            "approve_verification",
            "reject_verification",
        ]:
            return [IsAuthenticated(), CanReviewVerification()]
        if self.action == "documents":
            if self.request and self.request.method.upper() == "POST":
                return [IsAuthenticated(), IsShelterStaff()]
            return [IsAuthenticated(), IsShelterMember()]
        if self.action == "members":
            if self.request and self.request.method.upper() == "POST":
                return [IsAuthenticated(), CanInviteMembers()]
            return [IsAuthenticated(), IsShelterMember()]
        if self.action == "invitations":
            if self.request and self.request.method.upper() == "POST":
                return [IsAuthenticated(), CanInviteMembers()]
            return [IsAuthenticated(), IsShelterManager()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "list":
            return ShelterListSerializer
        if self.action == "create":
            return ShelterCreateSerializer
        if self.action == "partial_update":
            return ShelterUpdateSerializer
        return ShelterDetailSerializer

    def list(self, request: Request) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ShelterListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ShelterListSerializer(queryset, many=True)
        return api_response(data=serializer.data)

    @handle_domain_exceptions
    def create(self, request: Request) -> Response:
        serializer = ShelterCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shelter = ShelterService.create_shelter(
            user=(
                request.user if request.user.is_authenticated else User.objects.first()
            ),
            **serializer.validated_data,
        )
        return api_response(
            success=True,
            message="Shelter created successfully.",
            data=ShelterDetailSerializer(shelter).data,
            status_code=status.HTTP_201_CREATED,
        )

    @handle_domain_exceptions
    def retrieve(self, request: Request, pk: str = None) -> Response:
        try:
            shelter_id = _parse_uuid(pk)
        except NotFound:
            raise NotFound("Invalid shelter UUID.")

        shelter = get_shelter_by_id(shelter_id)
        if not shelter:
            raise NotFound("Shelter not found.")

        return api_response(data=ShelterDetailSerializer(shelter).data)

    @handle_domain_exceptions
    def partial_update(self, request: Request, pk: str = None) -> Response:
        try:
            shelter_id = _parse_uuid(pk)
        except NotFound:
            raise NotFound("Invalid shelter UUID.")

        serializer = ShelterUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_shelter = ShelterService.update_shelter(
            shelter_id, **serializer.validated_data
        )
        return api_response(
            message="Shelter profile updated successfully.",
            data=ShelterDetailSerializer(updated_shelter).data,
        )

    # --- Verification Workflow Actions ---

    @extend_schema(
        summary="Submit Shelter Verification",
        description="Submits active shelter verification workflow for review.",
        request=None,
        responses={200: ShelterVerificationSerializer},
    )
    @action(detail=True, methods=["post"], url_path="verification/submit")
    @handle_domain_exceptions
    def submit_verification(self, request: Request, pk: str = None) -> Response:
        shelter_id = _parse_uuid(pk)
        verification = get_active_verification(shelter_id)
        if not verification:
            return api_response(
                success=False,
                message="No active verification workflow found for this shelter.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        updated = VerificationService.submit_verification(verification.id)
        return api_response(
            message="Verification request submitted successfully.",
            data=ShelterVerificationSerializer(updated).data,
        )

    @extend_schema(
        summary="Start Review on Verification",
        description="Places a submitted verification workflow under review.",
        request=None,
        responses={200: ShelterVerificationSerializer},
    )
    @action(detail=True, methods=["post"], url_path="verification/start-review")
    @handle_domain_exceptions
    def start_review(self, request: Request, pk: str = None) -> Response:
        shelter_id = _parse_uuid(pk)
        verification = get_active_verification(shelter_id)
        if not verification:
            return api_response(
                success=False,
                message="No active verification request found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        updated = VerificationService.start_review(
            verification.id, reviewer_user=request.user
        )
        return api_response(
            message="Verification review started.",
            data=ShelterVerificationSerializer(updated).data,
        )

    @extend_schema(
        summary="Request Information for Verification",
        description="Requests additional details or documents for shelter verification.",
        request=VerificationRequestInfoSerializer,
        responses={200: ShelterVerificationSerializer},
    )
    @action(detail=True, methods=["post"], url_path="verification/request-information")
    @handle_domain_exceptions
    def request_information(self, request: Request, pk: str = None) -> Response:
        serializer = VerificationRequestInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shelter_id = _parse_uuid(pk)
        verification = get_active_verification(shelter_id)
        if not verification:
            return api_response(
                success=False,
                message="No active verification request found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        updated = VerificationService.request_information(
            verification.id,
            reviewer_user=request.user,
            notes=serializer.validated_data["notes"],
        )
        return api_response(
            message="Additional information requested successfully.",
            data=ShelterVerificationSerializer(updated).data,
        )

    @extend_schema(
        summary="Approve Shelter Verification",
        description="Approves shelter verification and updates operational status to VERIFIED.",
        request=VerificationApproveSerializer,
        responses={200: ShelterVerificationSerializer},
    )
    @action(detail=True, methods=["post"], url_path="verification/approve")
    @handle_domain_exceptions
    def approve_verification(self, request: Request, pk: str = None) -> Response:
        serializer = VerificationApproveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shelter_id = _parse_uuid(pk)
        verification = get_active_verification(shelter_id)
        if not verification:
            return api_response(
                success=False,
                message="No active verification request found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        updated = VerificationService.approve_verification(
            verification.id,
            reviewer_user=request.user,
            notes=serializer.validated_data.get("notes", ""),
        )
        return api_response(
            message="Shelter verification approved successfully.",
            data=ShelterVerificationSerializer(updated).data,
        )

    @extend_schema(
        summary="Reject Shelter Verification",
        description="Rejects shelter verification request with reason.",
        request=VerificationRejectSerializer,
        responses={200: ShelterVerificationSerializer},
    )
    @action(detail=True, methods=["post"], url_path="verification/reject")
    @handle_domain_exceptions
    def reject_verification(self, request: Request, pk: str = None) -> Response:
        serializer = VerificationRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shelter_id = _parse_uuid(pk)
        verification = get_active_verification(shelter_id)
        if not verification:
            return api_response(
                success=False,
                message="No active verification request found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        updated = VerificationService.reject_verification(
            verification.id,
            reviewer_user=request.user,
            reason=serializer.validated_data["reason"],
        )
        return api_response(
            message="Shelter verification rejected.",
            data=ShelterVerificationSerializer(updated).data,
        )

    # --- Document Sub-Resource Actions ---

    @extend_schema(
        methods=["get"],
        summary="List Shelter Documents",
        description="Returns uploaded verification documents for a shelter.",
        responses={200: ShelterDocumentSerializer(many=True)},
    )
    @extend_schema(
        methods=["post"],
        summary="Attach Shelter Document",
        description="Uploads and attaches a verification document to a shelter.",
        request=DocumentAttachSerializer,
        responses={201: ShelterDocumentSerializer},
    )
    @action(
        detail=True,
        methods=["get", "post"],
        url_path="documents",
        parser_classes=[MultiPartParser, FormParser],
    )
    @handle_domain_exceptions
    def documents(self, request: Request, pk: str = None) -> Response:
        if request.method == "POST":
            return self.attach_document(request, pk)
        return self.list_documents(request, pk)

    def list_documents(self, request: Request, pk: str = None) -> Response:
        shelter_id = _parse_uuid(pk)
        documents = list_shelter_documents(shelter_id)
        serializer = ShelterDocumentSerializer(documents, many=True)
        return api_response(data=serializer.data)

    def attach_document(self, request: Request, pk: str = None) -> Response:
        serializer = DocumentAttachSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shelter_id = _parse_uuid(pk)
        shelter = get_shelter_by_id(shelter_id)
        if not shelter:
            raise NotFound("Shelter not found.")

        verification = get_active_verification(shelter_id)
        document = VerificationService.attach_document(
            shelter=shelter,
            document_type=serializer.validated_data["document_type"],
            file=serializer.validated_data["file"],
            uploaded_by=request.user if request.user.is_authenticated else None,
            verification=verification,
        )
        return api_response(
            success=True,
            message="Document attached successfully.",
            data=ShelterDocumentSerializer(document).data,
            status_code=status.HTTP_201_CREATED,
        )

    # --- Member Sub-Resource Actions ---

    @extend_schema(
        methods=["get"],
        summary="List Shelter Members",
        description="Returns member associations for a shelter.",
        responses={200: ShelterMemberSerializer(many=True)},
    )
    @extend_schema(
        methods=["post"],
        summary="Add Shelter Member",
        description="Adds a user as a member of a shelter organization.",
        request=MemberAddSerializer,
        responses={201: ShelterMemberSerializer},
    )
    @action(detail=True, methods=["get", "post"], url_path="members")
    @handle_domain_exceptions
    def members(self, request: Request, pk: str = None) -> Response:
        if request.method == "POST":
            return self.add_member(request, pk)
        return self.list_members(request, pk)

    def list_members(self, request: Request, pk: str = None) -> Response:
        shelter_id = _parse_uuid(pk)
        members = get_shelter_members(shelter_id)
        role = request.query_params.get("role")
        if role:
            members = members.filter(role=role)
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            members = members.filter(is_active=is_active.lower() == "true")

        serializer = ShelterMemberSerializer(members, many=True)
        return api_response(data=serializer.data)

    def add_member(self, request: Request, pk: str = None) -> Response:
        serializer = MemberAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shelter_id = _parse_uuid(pk)
        shelter = get_shelter_by_id(shelter_id)
        if not shelter:
            raise NotFound("Shelter not found.")

        try:
            target_user = User.objects.get(id=serializer.validated_data["user_id"])
        except User.DoesNotExist:
            raise ValidationError({"user_id": "User not found."})

        member = MemberService.add_member(
            shelter=shelter,
            user=target_user,
            role=serializer.validated_data["role"],
        )
        return api_response(
            success=True,
            message="Member added successfully.",
            data=ShelterMemberSerializer(member).data,
            status_code=status.HTTP_201_CREATED,
        )

    # --- Invitation Sub-Resource Actions ---

    @extend_schema(
        methods=["get"],
        summary="List Shelter Invitations",
        description="Lists all staff/volunteer invitations for a shelter.",
        responses={200: ShelterInvitationSerializer(many=True)},
    )
    @extend_schema(
        methods=["post"],
        summary="Create Shelter Invitation",
        description="Dispatches a tokenized staff or volunteer invitation.",
        request=InvitationCreateSerializer,
        responses={201: ShelterInvitationSerializer},
    )
    @action(detail=True, methods=["get", "post"], url_path="invitations")
    @handle_domain_exceptions
    def invitations(self, request: Request, pk: str = None) -> Response:
        if request.method == "POST":
            return self.create_invitation(request, pk)
        return self.list_invitations(request, pk)

    def list_invitations(self, request: Request, pk: str = None) -> Response:
        shelter_id = _parse_uuid(pk)
        inv_qs = list_shelter_invitations(shelter_id)
        status_param = request.query_params.get("status")
        if status_param:
            inv_qs = inv_qs.filter(status=status_param)

        serializer = ShelterInvitationSerializer(inv_qs, many=True)
        return api_response(data=serializer.data)

    def create_invitation(self, request: Request, pk: str = None) -> Response:
        serializer = InvitationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shelter_id = _parse_uuid(pk)
        shelter = get_shelter_by_id(shelter_id)
        if not shelter:
            raise NotFound("Shelter not found.")

        invitation = InvitationService.create_invitation(
            shelter=shelter,
            email=serializer.validated_data["email"],
            role=serializer.validated_data["role"],
            invited_by=request.user if request.user.is_authenticated else None,
            expiry_days=serializer.validated_data.get("expiry_days", 7),
        )
        return api_response(
            success=True,
            message="Invitation created successfully.",
            data=ShelterInvitationSerializer(invitation).data,
            status_code=status.HTTP_201_CREATED,
        )


# --- Standalone Resource Views ---


@extend_schema(
    summary="Remove Shelter Document",
    description="Deletes an unapproved shelter verification document.",
    responses={200: None, 400: None},
)
class DocumentDetailAPIView(viewsets.ViewSet):
    """Standalone API view for single document operations."""

    permission_classes = [IsAuthenticated, CanDeleteDocument]

    @handle_domain_exceptions
    def destroy(self, request: Request, pk: str = None) -> Response:
        doc_id = _parse_uuid(pk)
        VerificationService.remove_document(doc_id)
        return api_response(message="Document deleted successfully.")


@extend_schema_view(
    partial_update=extend_schema(
        summary="Update Member Role",
        description="Updates membership role of a shelter staff member.",
        request=MemberUpdateSerializer,
        responses={200: ShelterMemberSerializer},
    ),
    destroy=extend_schema(
        summary="Remove Member",
        description="Removes a member from a shelter.",
        responses={200: None},
    ),
)
class MemberDetailAPIView(viewsets.ViewSet):
    """Standalone API view for single member role updates and deletion."""

    permission_classes = [IsAuthenticated, CanManageMember]

    @handle_domain_exceptions
    def partial_update(self, request: Request, pk: str = None) -> Response:
        serializer = MemberUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member_id = _parse_uuid(pk)
        updated = MemberService.change_role(
            member_id, new_role=serializer.validated_data["role"]
        )
        return api_response(
            message="Member role updated successfully.",
            data=ShelterMemberSerializer(updated).data,
        )

    @handle_domain_exceptions
    def destroy(self, request: Request, pk: str = None) -> Response:
        member_id = _parse_uuid(pk)
        MemberService.remove_member(member_id)
        return api_response(message="Member removed successfully.")


class InvitationStandaloneViewSet(viewsets.ViewSet):
    """Standalone ViewSet for global invitation accept and revoke actions."""

    def get_permissions(self):
        if self.action == "revoke_invitation":
            return [IsAuthenticated(), CanRevokeInvitation()]
        return [IsAuthenticated()]

    @extend_schema(
        summary="Accept Shelter Invitation",
        description="Accepts a shelter invitation token and creates membership.",
        request=InvitationAcceptSerializer,
        responses={200: ShelterMemberSerializer},
    )
    @action(detail=False, methods=["post"], url_path="accept")
    @handle_domain_exceptions
    def accept_invitation(self, request: Request) -> Response:
        serializer = InvitationAcceptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member = InvitationService.accept_invitation(
            token=serializer.validated_data["token"],
            user=(
                request.user if request.user.is_authenticated else User.objects.first()
            ),
        )
        return api_response(
            message="Invitation accepted successfully.",
            data=ShelterMemberSerializer(member).data,
        )

    @extend_schema(
        summary="Revoke Shelter Invitation",
        description="Revokes a pending shelter invitation.",
        request=InvitationRevokeSerializer,
        responses={200: ShelterInvitationSerializer},
    )
    @action(detail=False, methods=["post"], url_path="revoke")
    @handle_domain_exceptions
    def revoke_invitation(self, request: Request) -> Response:
        serializer = InvitationRevokeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invitation = InvitationService.revoke_invitation(
            invitation_id=serializer.validated_data["invitation_id"]
        )
        return api_response(
            message="Invitation revoked successfully.",
            data=ShelterInvitationSerializer(invitation).data,
        )

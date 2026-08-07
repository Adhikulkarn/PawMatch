"""
URL configuration for Shelter domain REST API endpoints under /api/v1/shelters/.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.shelters.api.views import (
    AdminVerificationViewSet,
    DocumentDetailAPIView,
    InvitationStandaloneViewSet,
    MemberDetailAPIView,
    ShelterDashboardAPIView,
    ShelterDocumentListAPIView,
    ShelterMeAPIView,
    ShelterRegisterAPIView,
    ShelterUploadDocumentAPIView,
    ShelterViewSet,
)

app_name = "shelters"

router = DefaultRouter()
router.register(r"", ShelterViewSet, basename="shelter")

urlpatterns = [
    # Top-level requested shelter dashboard endpoint
    path(
        "dashboard/",
        ShelterDashboardAPIView.as_view(),
        name="shelter-dashboard",
    ),
    # Administrator verification management endpoints
    path(
        "admin/verifications/pending/",
        AdminVerificationViewSet.as_view({"get": "pending"}),
        name="admin-verification-pending",
    ),
    path(
        "admin/verifications/<uuid:pk>/",
        AdminVerificationViewSet.as_view({"get": "retrieve"}),
        name="admin-verification-detail",
    ),
    path(
        "admin/verifications/<uuid:pk>/approve/",
        AdminVerificationViewSet.as_view({"post": "approve"}),
        name="admin-verification-approve",
    ),
    path(
        "admin/verifications/<uuid:pk>/reject/",
        AdminVerificationViewSet.as_view({"post": "reject"}),
        name="admin-verification-reject",
    ),
    path(
        "admin/verifications/<uuid:pk>/request-information/",
        AdminVerificationViewSet.as_view({"post": "request_information"}),
        name="admin-verification-request-info",
    ),
    # Top-level requested shelter domain endpoints
    path(
        "register/",
        ShelterRegisterAPIView.as_view(),
        name="shelter-register",
    ),
    path(
        "me/",
        ShelterMeAPIView.as_view(),
        name="shelter-me",
    ),
    path(
        "upload-document/",
        ShelterUploadDocumentAPIView.as_view(),
        name="shelter-upload-document",
    ),
    path(
        "documents/",
        ShelterDocumentListAPIView.as_view(),
        name="shelter-document-list",
    ),
    path(
        "documents/<uuid:pk>/",
        DocumentDetailAPIView.as_view({"delete": "destroy"}),
        name="document-detail",
    ),
    # Standalone member endpoint: PATCH & DELETE /api/v1/shelters/members/{id}/
    path(
        "members/<uuid:pk>/",
        MemberDetailAPIView.as_view({"patch": "partial_update", "delete": "destroy"}),
        name="member-detail",
    ),
    # Standalone invitation endpoints: POST /api/v1/shelters/invitations/accept/ and /revoke/
    path(
        "invitations/accept/",
        InvitationStandaloneViewSet.as_view({"post": "accept_invitation"}),
        name="invitation-accept",
    ),
    path(
        "invitations/revoke/",
        InvitationStandaloneViewSet.as_view({"post": "revoke_invitation"}),
        name="invitation-revoke",
    ),
    path("", include(router.urls)),
]

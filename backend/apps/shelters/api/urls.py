"""
URL configuration for Shelter domain REST API endpoints under /api/v1/shelters/.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.shelters.api.views import (
    DocumentDetailAPIView,
    InvitationStandaloneViewSet,
    MemberDetailAPIView,
    ShelterViewSet,
)

app_name = "shelters"

router = DefaultRouter()
router.register(r"", ShelterViewSet, basename="shelter")

urlpatterns = [
    # Standalone document endpoint: DELETE /api/v1/shelters/documents/{id}/
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

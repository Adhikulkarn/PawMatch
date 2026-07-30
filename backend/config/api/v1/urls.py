"""
Version 1 router.

Aggregates URL configs from every application.
Each app owns its own api/urls.py — only routing is registered here.
"""

from django.urls import include, path

urlpatterns = [
    path("core/", include("apps.core.api.urls")),
    path("accounts/", include("apps.accounts.api.urls")),
    path("shelters/", include("apps.shelters.api.urls")),
    path("pets/", include("apps.pets.api.urls")),
    path("adoptions/", include("apps.adoptions.api.urls")),
    path("notifications/", include("apps.notifications.api.urls")),
    path("administration/", include("apps.administration.api.urls")),
    path("audit-logs/", include("apps.audit_logs.api.urls")),
]

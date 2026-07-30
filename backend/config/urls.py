"""
Project root URL configuration.

Only project-level routes belong here:
    - Health checks (Render / Cloud Orchestration)
    - Admin site
    - API gateway
"""
from django.contrib import admin
from django.urls import include, path
from apps.core.api.views import health_check

urlpatterns = [
    path("health/", health_check, name="root_health_check"),
    path("admin/", admin.site.urls),
    path("api/", include("config.api.urls")),
]

"""
Project root URL configuration.

Only project-level routes belong here:
    - Admin site
    - API gateway
    - Health checks (future)
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("config.api.urls")),
]

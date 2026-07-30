"""
Central API gateway.

All API versions are registered here.
New versions are added as:
    path("v2/", include("config.api.v2.urls")),
"""

from django.urls import include, path

urlpatterns = [
    path("v1/", include("config.api.v1.urls")),
]

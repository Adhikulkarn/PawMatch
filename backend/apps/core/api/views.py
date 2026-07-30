"""
Core infrastructure API views for PawMatch.
"""

import os
from datetime import datetime, timezone

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Module-level static Context Caching for sub-millisecond response performance
_APP_VERSION = os.getenv("APP_VERSION", os.getenv("RENDER_GIT_COMMIT", "1.0.0"))


def _get_environment_name() -> str:
    env_override = os.getenv("ENVIRONMENT")
    if env_override:
        return env_override
    settings_module = getattr(
        settings, "SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "")
    )
    if "production" in settings_module:
        return "production"
    elif "staging" in settings_module:
        return "staging"
    return "development"


_ENVIRONMENT_NAME = _get_environment_name()


@require_http_methods(["GET", "HEAD"])
def health_check(request):
    """
    Ultra-lightweight health check endpoint for cloud orchestrators (Render, ECS, K8s).
    Supports GET and HEAD HTTP methods for zero-payload network health probing.
    Returns HTTP 200 with service metadata in < 1 ms without database interaction.
    """
    payload = {
        "status": "healthy",
        "service": "pawmatch-backend",
        "version": _APP_VERSION,
        "environment": _ENVIRONMENT_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return JsonResponse(payload, status=200)

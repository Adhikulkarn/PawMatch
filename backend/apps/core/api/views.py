"""
Core infrastructure API views for PawMatch.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health_check(request):
    """
    Lightweight health check endpoint for cloud orchestrator probes (Render, ECS, K8s).
    Returns HTTP 200 instantly without database queries or authentication checks.
    """
    return JsonResponse({"status": "healthy"}, status=200)

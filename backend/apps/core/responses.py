"""
Standardized API Response utilities for PawMatch.
"""

from typing import Any, Optional

from rest_framework import status
from rest_framework.response import Response


def api_response(
    success: bool = True,
    message: str = "",
    data: Optional[Any] = None,
    errors: Optional[Any] = None,
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Constructs a standardized JSON response for PawMatch REST endpoints.
    Format:
    {
        "success": true | false,
        "message": "...",
        "data": { ... } | null,
        "errors": { ... } | null
    }
    """
    payload = {
        "success": success,
        "message": message,
    }
    if data is not None:
        payload["data"] = data
    if errors is not None:
        payload["errors"] = errors
    return Response(payload, status=status_code)

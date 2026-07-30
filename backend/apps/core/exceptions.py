"""
Custom DRF exception handler for standardized error response structures.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Standardizes error responses across all DRF API endpoints.
    Format:
    {
        "success": False,
        "error": {
            "type": "ValidationError",
            "status_code": 400,
            "message": "...",
            "details": {...}
        }
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "status_code": response.status_code,
                "message": getattr(exc, "detail", str(exc)),
                "details": (
                    response.data
                    if isinstance(response.data, dict)
                    else {"non_field_errors": response.data}
                ),
            },
        }
        response.data = custom_data

    return response

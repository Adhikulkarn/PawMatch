"""
Custom DRF exception handler for standardized error response structures.
"""

from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Standardizes error responses across all DRF API endpoints.
    Format:
    {
        "success": False,
        "message": "...",
        "errors": { ... }
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Extract user-friendly error message
        if hasattr(exc, "detail") and isinstance(exc.detail, str):
            message = exc.detail
        elif (
            hasattr(exc, "detail")
            and isinstance(exc.detail, dict)
            and "detail" in exc.detail
        ):
            message = str(exc.detail["detail"])
        elif hasattr(exc, "detail") and isinstance(exc.detail, list) and exc.detail:
            message = str(exc.detail[0])
        elif isinstance(response.data, dict) and "detail" in response.data:
            message = str(response.data["detail"])
        elif isinstance(response.data, list) and response.data:
            message = str(response.data[0])
        else:
            message = "An error occurred while processing your request."

        # Structure errors dictionary
        if isinstance(response.data, dict):
            errors = response.data
        elif isinstance(response.data, list):
            errors = {"non_field_errors": response.data}
        else:
            errors = {"detail": str(response.data)}

        # Build standardized error payload
        custom_data = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        response.data = custom_data

    return response

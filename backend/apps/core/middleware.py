"""
Core infrastructure middleware for PawMatch.
"""

import logging
import threading
import uuid

from django.utils.deprecation import MiddlewareMixin

# Thread-local context storage for request tracing
_thread_locals = threading.local()


def get_current_request_id() -> str:
    """Returns the current thread's active request ID or '-'."""
    return getattr(_thread_locals, "request_id", "-")


class RequestIDFilter(logging.Filter):
    """
    Logging filter that injects the current request_id into Python log records.
    """

    def filter(self, record):
        record.request_id = get_current_request_id()
        return True


class RequestIDMiddleware(MiddlewareMixin):
    """
    Middleware that extracts or generates a unique Request ID (UUIDv4) for every HTTP request.
    Attaches the request_id to thread-local context, request object, and outgoing response headers.
    """

    def process_request(self, request):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        request.request_id = request_id
        _thread_locals.request_id = request_id

    def process_response(self, request, response):
        request_id = getattr(request, "request_id", None) or get_current_request_id()
        if request_id and request_id != "-":
            response["X-Request-ID"] = request_id
        # Clean up thread-local storage to prevent leakage across pooled threads
        _thread_locals.request_id = "-"
        return response

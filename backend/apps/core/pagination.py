"""
Core pagination classes for PawMatch REST APIs.
"""

from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """Standardized page-number pagination for catalog endpoints."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class StandardLimitOffsetPagination(LimitOffsetPagination):
    """Limit-offset pagination for high-volume feed endpoints."""

    default_limit = 20
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 100

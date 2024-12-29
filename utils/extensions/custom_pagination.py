from django.utils.translation import gettext_lazy as _
from rest_framework import pagination, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class NotFoundExtended(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("A server error occurred.")
    default_code = "error"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = str(self.default_detail)
        if code is None:
            code = str(self.default_code)

        self.detail = detail


class CustomPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"  # items per page

    def get_paginated_response(self, data):
        if hasattr(self, "page"):
            return Response(
                {
                    "links": {
                        "next": self.get_next_link(),
                        "previous": self.get_previous_link(),
                    },
                    "count": self.page.paginator.count,
                    "total_pages": self.page.paginator.num_pages,
                    "results": data,
                }
            )
        else:
            return Response(
                {
                    "links": {},
                    "count": len(data),
                    "total_pages": 0,
                    "results": data,
                }
            )

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate the queryset, but return all results if a specific query parameter is provided.
        """
        if "all" in request.query_params:
            return None
        return super().paginate_queryset(queryset, request, view)

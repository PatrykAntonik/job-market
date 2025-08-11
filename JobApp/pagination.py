from rest_framework.pagination import PageNumberPagination


class OptionalPagination(PageNumberPagination):
    """
    Custom pagination class that allows for optional pagination.
    """

    page_size = 10
    page_size_query_param = "page_size"

    def get_page_size(self, request):
        no_paginate = request.query_params.get("no_pagination", "false").lower()
        if no_paginate == "true":
            return None
        return super().get_page_size(request)

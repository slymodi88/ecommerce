from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size', 20)
        return page_size

    def get_paginated_response(self, data):
        if data:
            return Response({
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count,
                'num_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'result': data,
                'status': True,
                'message': 'Retrieved Successfully'
            }, status=200)
        else:
            return Response({
                'result': [],
                'status': True,
                'message': 'Retrieved Successfully'
            }, status=200)


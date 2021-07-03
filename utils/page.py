from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict


# 自定义分页
class CustomPagination(PageNumberPagination): 
    """
    分页
    """ 
    page_size = 20
    page_size_query_param = 'limit'  
    page_query_param = "page"  
    max_page_size = 100 

    def get_paginated_response(self, data):
        code = 200
        msg = ''
        if not data:
            code = 404
            msg = "data not found"

        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),
            ('count', self.page.paginator.count),
            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            ('data', data)
        ]))


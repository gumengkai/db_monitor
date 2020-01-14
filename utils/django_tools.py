# encoding: utf-8

from rest_framework.pagination import PageNumberPagination

class NoPagination(PageNumberPagination):
    page_size = 99999 # 表示每页的默认显示数量
    page_size_query_param = 'page_size' # 表示url中每页数量参数
    page_query_param = 'p' # 表示url中的页码参数
    max_page_size = 99999  # 表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃

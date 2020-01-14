from django.shortcuts import render

from .models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from utils.tools import get_utctime,today,last_day
from utils.django_tools import NoPagination

class ApiMysqlStat(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        return MysqlStat.objects.filter(status=0, tags=tags).order_by('-status')
    serializer_class = MysqlStatSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiMysqlStatHis(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        start_time = self.request.query_params.get('start_time',None)
        end_time = self.request.query_params.get('end_time',None)
        if start_time and end_time:
            start_time = get_utctime(start_time)
            end_time = get_utctime(end_time)
        else:
            # default data of 1 day
            end_time = today()
            start_time = last_day()
        return MysqlStatHis.objects.filter(tags=tags, check_time__gte=start_time, check_time__lte=end_time).order_by('check_time')

    serializer_class = MysqlStatSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

# all instance
class ApiMysqlStatList(generics.ListCreateAPIView):
    queryset = MysqlStat.objects.get_queryset().order_by('-id')
    serializer_class = MysqlStatSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host','status')
    search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)


class ApiMysqlSlowquery(generics.ListCreateAPIView):
    queryset = MysqlSlowquery.objects.get_queryset().order_by('-id')
    serializer_class = MysqlSlowquerySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host',)
    search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)

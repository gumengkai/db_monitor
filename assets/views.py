# encoding:utf-8

from .models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *

# Ecs Api           drf 中文文档   http://drf.jiuyou.info/#/drf/requests
class ApiOracleList(generics.ListCreateAPIView):
    queryset = OracleList.objects.get_queryset().order_by('id')
    serializer_class = OracleListSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host','db_version')
    search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)  # 继承 django的权限

class ApiOracleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OracleList.objects.get_queryset().order_by('id')
    serializer_class = OracleListSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiMysqlList(generics.ListCreateAPIView):
    queryset = MysqlList.objects.get_queryset().order_by('id')
    serializer_class = MysqlListSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host','db_version')
    search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)  # 继承 django的权限

class ApiMysqlDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MysqlList.objects.get_queryset().order_by('id')
    serializer_class = MysqlListSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiLinuxList(generics.ListCreateAPIView):
    queryset = LinuxList.objects.get_queryset().order_by('id')
    serializer_class = LinuxListSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host','linux_version')
    search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)  # 继承 django的权限

class ApiLinuxDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LinuxList.objects.get_queryset().order_by('id')
    serializer_class = LinuxListSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class ApiRedisList(generics.ListCreateAPIView):
    queryset = RedisList.objects.get_queryset().order_by('id')
    serializer_class = RedisListSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host','redis_version')
    search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)  # 继承 django的权限

class ApiRedisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RedisList.objects.get_queryset().order_by('id')
    serializer_class = RedisListSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

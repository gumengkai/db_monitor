from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from utils.tools import *
from utils.django_tools import NoPagination
from django.http import HttpResponse
from django.core import serializers
from utils.redis_base import RedisBase
import redis
import json
import numpy as np

# Create your views here.

class ApiRedisStat(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        return RedisStat.objects.filter(status=0, tags=tags).order_by('-status')
    serializer_class = RedisStatSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiRedisStatHis(generics.ListCreateAPIView):
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
        return RedisStatHis.objects.filter(tags=tags, check_time__gte=start_time, check_time__lte=end_time).order_by('check_time')

    serializer_class = RedisStatSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

# all instance
class ApiRedisStatList(generics.ListCreateAPIView):
    queryset = RedisStat.objects.get_queryset().order_by('-id')
    serializer_class = RedisStatSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host','status')
    search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiRedisConfig(generics.ListAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        redis_conn = redis.StrictRedis(host='192.168.48.60', port=6379)
        redis_config =  redis_conn.config_get()
        print(type(redis_config))
        serializer_class = RedisConfigSerializer
        return redis_config

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiRedisConfig(request):
    tags = request.GET.get('tags')
    paraname = request.GET.get('paraname')
    redis_params = get_redis_params(tags)
    redis_conn = RedisBase(redis_params).connection()
    redis_config = redis_conn.config_get(paraname) if paraname else redis_conn.config_get()
    print(type(redis_config))
    return HttpResponse(json.dumps(redis_config))


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiRedisSlowLog(request):
    tags = request.GET.get('tags')
    redis_params = get_redis_params(tags)
    redis_conn = RedisBase(redis_params).connection()
    redis_slowlog = redis_conn.slowlog_get()
    dic_res = {each['id']:each for each in redis_slowlog}
    return HttpResponse(json.dumps(dic_res,cls=MyEncoder))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiRedisClientList(request):
    tags = request.GET.get('tags')
    redis_params = get_redis_params(tags)
    redis_conn = RedisBase(redis_params).connection()
    redis_client_list = redis_conn.client_list()
    dic_res = {each['id']:each for each in redis_client_list}
    return HttpResponse(json.dumps(dic_res,cls=MyEncoder))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiRedisImmediateStats(request):
    tags = request.GET.get('tags')
    redis_params = get_redis_params(tags)
    redis_conn = RedisBase(redis_params).connection()
    redis_info_all = {
        'Keyspace':redis_conn.info('Keyspace'),
        'Stats':redis_conn.info('Stats'),
        'Persistence':redis_conn.info('Persistence'),
        'CPU':redis_conn.info('CPU'),
        'Clients':redis_conn.info('Clients'),
        'Memory':redis_conn.info('Memory'),
        'Server':redis_conn.info('Server'),
        'Replication':redis_conn.info('Replication'),
        'Commandstats':redis_conn.info('Commandstats')
    }
    return HttpResponse(json.dumps(redis_info_all))

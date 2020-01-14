from django.shortcuts import render

# Create your views here.
from .models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from utils.tools import get_utctime,today,last_day
from utils.django_tools import NoPagination

class ApiLinuxStat(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        return LinuxStat.objects.filter(status=0, tags=tags).order_by('status')
    serializer_class = LinuxStatSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiLinuxStatHis(generics.ListCreateAPIView):
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
        return LinuxStatHis.objects.filter(tags=tags, check_time__gte=start_time, check_time__lte=end_time).order_by('check_time')

    serializer_class = LinuxStatHisSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

# all instance
class ApiLinuxStatList(generics.ListCreateAPIView):
    queryset = LinuxStat.objects.get_queryset().order_by('-status')
    serializer_class = LinuxStatSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host','status')
    search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiLinuxDisk(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        return LinuxDisk.objects.filter(tags=tags).order_by('-used_percent')
    serializer_class = LinuxDiskSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiLinuxDiskHis(generics.ListCreateAPIView):
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
        return LinuxDiskHis.objects.filter(tags=tags, check_time__gte=start_time, check_time__lte=end_time).order_by('check_time')

    serializer_class = LinuxDiskSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiLinuxIoStat(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        return LinuxIoStat.objects.filter(tags=tags)
    serializer_class = LinuxIoStatSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiLinuxIoStatHis(generics.ListCreateAPIView):
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
        return LinuxIoStatHis.objects.filter(tags=tags, check_time__gte=start_time, check_time__lte=end_time).order_by('check_time')

    serializer_class = LinuxIoStatSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

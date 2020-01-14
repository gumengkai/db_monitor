from rest_framework import serializers
from .models import *

class LinuxStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinuxStat
        fields = '__all__'

class LinuxStatHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinuxStatHis
        fields = '__all__'

class LinuxDiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinuxDisk
        fields = '__all__'

class LinuxDiskHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinuxDiskHis
        fields = '__all__'

class LinuxIoStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinuxIoStat
        fields = '__all__'

class LinuxIoStatHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinuxIoStatHis
        fields = '__all__'

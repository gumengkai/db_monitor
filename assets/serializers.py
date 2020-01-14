from rest_framework import serializers
from .models import *


class OracleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleList
        fields = '__all__'

class MysqlListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MysqlList
        fields = '__all__'

class LinuxListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinuxList
        fields = '__all__'

class RedisListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedisList
        fields = '__all__'

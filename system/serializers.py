from rest_framework import serializers
from .models import AlertLog,AlarmConf,AlarmInfo,SetupLog

class AlertLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertLog
        fields = '__all__'


class AlarmConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmConf
        fields = '__all__'


class AlarmInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmInfo
        fields = '__all__'

class SetupLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetupLog
        fields = '__all__'

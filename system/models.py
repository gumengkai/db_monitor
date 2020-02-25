from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User
from django.utils import timezone

# Create your models here.

class Users(AbstractUser):
    position = models.CharField(max_length=64, verbose_name='职位信息', blank=True, null=True)
    avatar = models.CharField(max_length=256, verbose_name='头像', blank=True, null=True)
    mobile = models.CharField(max_length=11, verbose_name='手机', blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class AlertLog(models.Model):

    LOG_LEVEL = [
        ('error', 'error'),
        ('warn', 'warn'),
        ('info', 'info')
    ]

    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    type = models.CharField("采集源类型 1:Oracle数据库 2:MySQL数据库 3:Redis 4:Linux",max_length=16)
    log_time = models.CharField("日志时间",max_length=255)
    log_level = models.CharField("日志级别",max_length=16,choices=LOG_LEVEL)
    log_content = models.TextField("日志内容")
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'alert_log'
        verbose_name = "日志解析采集数据"
        verbose_name_plural = verbose_name

class AlarmConf(models.Model):
    type = models.IntegerField("采集源类型 1:Oracle数据库 2:MySQL数据库 3:Redis 4:Linux")
    name = models.CharField("告警名称",max_length=128)
    judge = models.CharField("判断条件",max_length=8)
    judge_value = models.FloatField("判断阈值")
    judge_des = models.CharField("判断描述",max_length=128)
    judge_table = models.CharField("数据来源表",max_length=128,blank=True,null=True)
    judge_sql = models.TextField("判断SQL")
    conf_table = models.CharField("配置表(用于检测是否告警屏蔽)",max_length=128,blank=True,null=True)
    conf_column = models.CharField("配置表字段(用于检测是否告警屏蔽)",max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'alarm_conf'
        verbose_name = "告警配置"
        verbose_name_plural = verbose_name

class AlarmInfo(models.Model):
    tags = models.CharField("标签",max_length=32)
    url = models.CharField("连接地址",max_length=255)
    alarm_type = models.CharField("告警类型",max_length=255)
    alarm_header = models.CharField("告警标题",max_length=255)
    alarm_content = models.TextField("告警标题",)
    alarm_time = models.DateTimeField("告警时间")

    class Meta:
        db_table = 'alarm_info'
        verbose_name = "告警信息"
        verbose_name_plural = verbose_name

class AlarmInfoHis(models.Model):
    tags = models.CharField("标签",max_length=32)
    url = models.CharField("连接地址",max_length=255)
    alarm_type = models.CharField("告警类型",max_length=255)
    alarm_header = models.CharField("告警标题",max_length=255)
    alarm_content = models.TextField("告警标题",)
    alarm_time = models.DateTimeField("告警时间")

    class Meta:
        db_table = 'alarm_info_his'
        verbose_name = "告警信息"
        verbose_name_plural = verbose_name

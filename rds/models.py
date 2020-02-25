from django.db import models
from django.utils import timezone

# Create your models here.

class RedisStat(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("端口号",default=1521)
    version = models.CharField("redis版本",max_length=64,blank=True,null=True)
    redis_mode = models.CharField("redis模式",max_length=128,blank=True,null=True)
    role = models.CharField("角色",max_length=32,blank=True,null=True)
    updays = models.IntegerField("运行天数",blank=True,null=True)
    slaves = models.IntegerField("slave数量",blank=True,null=True)
    maxmemory = models.FloatField("最大内存",blank=True,null=True)
    used_memory = models.FloatField("使用内存",blank=True,null=True)
    mem_fragmentation_ratio = models.FloatField("内存碎片率",blank=True,null=True)
    total_keys = models.IntegerField("键数量",blank=True,null=True)
    expire_keys = models.IntegerField("过期键数量",blank=True,null=True)
    connected_clients = models.IntegerField("连接数",blank=True,null=True)
    hits_all = models.IntegerField("命中数(累计)",blank=True,null=True)
    misses_all = models.IntegerField("未命中数(累计)",blank=True,null=True)
    expired_keys = models.IntegerField("过期键数量(实时)",blank=True,null=True)
    evicted_keys = models.IntegerField("被驱逐键数量(实时)",blank=True,null=True)
    hits = models.IntegerField("命中数(实时)",blank=True,null=True)
    misses = models.IntegerField("未命中数(实时)",blank=True,null=True)
    command_count = models.IntegerField("执行命令次数(实时)",blank=True,null=True)
    net_input_byte = models.FloatField(blank=True, null=True)
    net_out_byte = models.FloatField(blank=True, null=True)
    aof_delayed_fsync = models.FloatField("")
    cmdstat_brpop = models.FloatField(blank=True, null=True)
    cmdstat_publish = models.FloatField(blank=True, null=True)
    cmdstat_setnx = models.FloatField(blank=True, null=True)
    cmdstat_exec = models.FloatField(blank=True, null=True)
    cmdstat_multi = models.FloatField(blank=True, null=True)
    status = models.IntegerField("数据库连接状态 0成功 1失败",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'redis_stat'
        verbose_name = "Redis采集数据"
        verbose_name_plural = verbose_name

class RedisStatHis(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("端口号",default=1521)
    version = models.CharField("redis版本",max_length=64,blank=True,null=True)
    redis_mode = models.CharField("redis模式",max_length=128,blank=True,null=True)
    role = models.CharField("角色",max_length=32,blank=True,null=True)
    updays = models.IntegerField("运行天数",blank=True,null=True)
    slaves = models.IntegerField("slave数量",blank=True,null=True)
    maxmemory = models.FloatField("最大内存",blank=True,null=True)
    used_memory = models.FloatField("使用内存",blank=True,null=True)
    mem_fragmentation_ratio = models.FloatField("内存碎片率",blank=True,null=True)
    total_keys = models.IntegerField("键数量",blank=True,null=True)
    expire_keys = models.IntegerField("过期键数量",blank=True,null=True)
    connected_clients = models.IntegerField("连接数",blank=True,null=True)
    hits_all = models.IntegerField("命中数(累计)",blank=True,null=True)
    misses_all = models.IntegerField("未命中数(累计)",blank=True,null=True)
    expired_keys = models.IntegerField("过期键数量(实时)",blank=True,null=True)
    evicted_keys = models.IntegerField("被驱逐键数量(实时)",blank=True,null=True)
    hits = models.IntegerField("命中数(实时)",blank=True,null=True)
    misses = models.IntegerField("未命中数(实时)",blank=True,null=True)
    command_count = models.IntegerField("执行命令次数(实时)",blank=True,null=True)
    net_input_byte = models.FloatField(blank=True, null=True)
    net_out_byte = models.FloatField(blank=True, null=True)
    aof_delayed_fsync = models.FloatField("")
    cmdstat_brpop = models.FloatField(blank=True, null=True)
    cmdstat_publish = models.FloatField(blank=True, null=True)
    cmdstat_setnx = models.FloatField(blank=True, null=True)
    cmdstat_exec = models.FloatField(blank=True, null=True)
    cmdstat_multi = models.FloatField(blank=True, null=True)
    status = models.IntegerField("数据库连接状态 0成功 1失败",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'redis_stat_his'
        verbose_name = "Redis采集数据"
        verbose_name_plural = verbose_name

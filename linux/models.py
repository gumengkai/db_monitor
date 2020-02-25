from django.db import models
# Create your models here.
from django.utils import timezone

class LinuxStat(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("ssh端口号",default=22)
    hostname = models.CharField("主机名",max_length=64,blank=True,null=True)
    ipinfo = models.CharField("IP地址信息",max_length=255,blank=True, null=True)
    linux_version = models.CharField("linux版本",max_length=64,blank=True,null=True)
    updays = models.FloatField("启动天数",blank=True, null=True)
    kernel = models.CharField("内核版本",max_length=64,blank=True,null=True)
    frame = models.CharField("系统架构",max_length=64,blank=True,null=True)
    cpu_mode = models.CharField("CPU型号",max_length=64,blank=True, null=True)
    cpu_cache = models.CharField("CPU cache",max_length=64,blank=True, null=True)
    processor = models.CharField("CPU核心数",max_length=64,blank=True, null=True)
    cpu_speed = models.CharField("CPU频率",max_length=64,blank=True, null=True)
    recv_kbps = models.FloatField("接收流量",blank=True, null=True)
    send_kbps = models.FloatField("发送流量",blank=True, null=True)
    load1 = models.FloatField(blank=True, null=True)
    load5 = models.FloatField(blank=True, null=True)
    load15 = models.FloatField(blank=True, null=True)
    cpu_sys = models.FloatField(blank=True, null=True)
    cpu_iowait = models.FloatField(blank=True, null=True)
    cpu_user = models.FloatField(blank=True, null=True)
    cpu_used = models.FloatField("CPU使用率",blank=True, null=True)
    memtotal = models.FloatField("内存总大小",blank=True, null=True)
    mem_used = models.FloatField("内存使用率",blank=True, null=True)
    mem_cache = models.FloatField(blank=True, null=True)
    mem_buffer = models.FloatField(blank=True, null=True)
    mem_free = models.FloatField(blank=True, null=True)
    mem_used_mb = models.FloatField(blank=True, null=True)
    swap_used = models.FloatField(blank=True, null=True)
    swap_free = models.FloatField(blank=True, null=True)
    swapin = models.FloatField(blank=True, null=True)
    swapout = models.FloatField(blank=True, null=True)
    pgin = models.FloatField(blank=True, null=True)
    pgout = models.FloatField(blank=True, null=True)
    pgfault = models.FloatField(blank=True, null=True)
    pgmjfault = models.FloatField(blank=True, null=True)
    tcp_close = models.FloatField(blank=True, null=True)
    tcp_timewait = models.FloatField(blank=True, null=True)
    tcp_connected = models.FloatField(blank=True, null=True)
    tcp_syn = models.FloatField(blank=True, null=True)
    tcp_listen = models.FloatField(blank=True, null=True)
    iops = models.FloatField(blank=True, null=True)
    read_mb = models.FloatField(blank=True, null=True)
    write_mb = models.FloatField(blank=True, null=True)
    proc_new = models.FloatField(blank=True, null=True)
    proc_running = models.FloatField(blank=True, null=True)
    proc_block = models.FloatField(blank=True, null=True)
    intr = models.FloatField(blank=True, null=True)
    ctx = models.FloatField(blank=True, null=True)
    softirq = models.FloatField(blank=True, null=True)
    status = models.IntegerField("linux主机连接状态 0成功 1失败",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_stat'
        verbose_name = "Linux主机采集数据"
        verbose_name_plural = verbose_name


class LinuxDisk(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    dev = models.CharField("设备",max_length=64,blank=True,null=True)
    total_size = models.FloatField("总空间大小",blank=True, null=True)
    used_size = models.FloatField("使用空间大小",blank=True, null=True)
    free_size = models.FloatField("剩余空间大小",blank=True,null=True)
    used_percent = models.FloatField("使用率",blank=True,null=True)
    mount_point = models.CharField("挂载点",max_length=256,blank=True,null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_disk'
        verbose_name = "Linux磁盘信息采集数据"
        verbose_name_plural = verbose_name

class LinuxIoStat(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    dev = models.CharField("设备",max_length=64,blank=True,null=True)
    rd_s = models.FloatField("每秒读请求数",blank=True, null=True)
    rd_avgkb = models.FloatField("读请求平均大小",blank=True, null=True)
    rd_m_s = models.FloatField("每秒读大小(mb)",blank=True, null=True)
    rd_mrg_s = models.FloatField("每秒读合并(百分比)",blank=True, null=True)
    rd_cnc = models.FloatField("读并发数",blank=True, null=True)
    rd_rt = models.FloatField("读响应时间",blank=True, null=True)
    wr_s = models.FloatField("每秒写请求数",blank=True, null=True)
    wr_avgkb = models.FloatField("写请求平均大小",blank=True, null=True)
    wr_m_s = models.FloatField("每秒写大小(mb)",blank=True, null=True)
    wr_mrg_s = models.FloatField("每秒写合并(百分比)",blank=True, null=True)
    wr_cnc = models.FloatField("写并发数",blank=True, null=True)
    wr_rt = models.FloatField("写相应时间",blank=True, null=True)
    busy = models.FloatField("%util",blank=True, null=True)
    in_prg = models.FloatField("排队请求数",blank=True, null=True)
    io_s = models.FloatField("物理磁盘吞吐量",blank=True, null=True)
    qtime = models.FloatField("IO请求队列时间(平均排队时间)",blank=True, null=True)
    stime = models.FloatField("IO请求服务时间",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_io_stat'
        verbose_name = "Linux磁盘IO信息"
        verbose_name_plural = verbose_name


class LinuxStatHis(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("ssh端口号",default=22)
    hostname = models.CharField("主机名",max_length=64,blank=True,null=True)
    ipinfo = models.CharField("IP地址信息",max_length=255,blank=True, null=True)
    linux_version = models.CharField("linux版本",max_length=64,blank=True,null=True)
    updays = models.FloatField("启动天数",blank=True, null=True)
    kernel = models.CharField("内核版本",max_length=64,blank=True,null=True)
    frame = models.CharField("系统架构",max_length=64,blank=True,null=True)
    cpu_mode = models.CharField("CPU型号",max_length=64,blank=True, null=True)
    cpu_cache = models.CharField("CPU cache",max_length=64,blank=True, null=True)
    processor = models.CharField("CPU核心数",max_length=64,blank=True, null=True)
    cpu_speed = models.CharField("CPU频率",max_length=64,blank=True, null=True)
    recv_kbps = models.FloatField("接收流量",blank=True, null=True)
    send_kbps = models.FloatField("发送流量",blank=True, null=True)
    load1 = models.FloatField(blank=True, null=True)
    load5 = models.FloatField(blank=True, null=True)
    load15 = models.FloatField(blank=True, null=True)
    cpu_sys = models.FloatField(blank=True, null=True)
    cpu_iowait = models.FloatField(blank=True, null=True)
    cpu_user = models.FloatField(blank=True, null=True)
    cpu_used = models.FloatField("CPU使用率",blank=True, null=True)
    memtotal = models.FloatField("内存总大小",blank=True, null=True)
    mem_used = models.FloatField("内存使用率",blank=True, null=True)
    mem_cache = models.FloatField(blank=True, null=True)
    mem_buffer = models.FloatField(blank=True, null=True)
    mem_free = models.FloatField(blank=True, null=True)
    mem_used_mb = models.FloatField(blank=True, null=True)
    swap_used = models.FloatField(blank=True, null=True)
    swap_free = models.FloatField(blank=True, null=True)
    swapin = models.FloatField(blank=True, null=True)
    swapout = models.FloatField(blank=True, null=True)
    pgin = models.FloatField(blank=True, null=True)
    pgout = models.FloatField(blank=True, null=True)
    pgfault = models.FloatField(blank=True, null=True)
    pgmjfault = models.FloatField(blank=True, null=True)
    tcp_close = models.FloatField(blank=True, null=True)
    tcp_timewait = models.FloatField(blank=True, null=True)
    tcp_connected = models.FloatField(blank=True, null=True)
    tcp_syn = models.FloatField(blank=True, null=True)
    tcp_listen = models.FloatField(blank=True, null=True)
    iops = models.FloatField(blank=True, null=True)
    read_mb = models.FloatField(blank=True, null=True)
    write_mb = models.FloatField(blank=True, null=True)
    proc_new = models.FloatField(blank=True, null=True)
    proc_running = models.FloatField(blank=True, null=True)
    proc_block = models.FloatField(blank=True, null=True)
    intr = models.FloatField(blank=True, null=True)
    ctx = models.FloatField(blank=True, null=True)
    softirq = models.FloatField(blank=True, null=True)
    status = models.IntegerField("linux主机连接状态 0成功 1失败",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_stat_his'
        verbose_name = "Linux主机采集数据"
        verbose_name_plural = verbose_name


class LinuxDiskHis(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    dev = models.CharField("设备",max_length=64,blank=True,null=True)
    total_size = models.FloatField("总空间大小",blank=True, null=True)
    used_size = models.FloatField("使用空间大小",blank=True, null=True)
    free_size = models.FloatField("剩余空间大小",blank=True,null=True)
    used_percent = models.FloatField("使用率",blank=True,null=True)
    mount_point = models.CharField("挂载点",max_length=256,blank=True,null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_disk_his'
        verbose_name = "Linux磁盘信息采集数据"
        verbose_name_plural = verbose_name

class LinuxIoStatHis(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    dev = models.CharField("设备",max_length=64,blank=True,null=True)
    rd_s = models.FloatField("每秒读请求数",blank=True, null=True)
    rd_avgkb = models.FloatField("读请求平均大小",blank=True, null=True)
    rd_m_s = models.FloatField("每秒读大小(mb)",blank=True, null=True)
    rd_mrg_s = models.FloatField("每秒读合并(百分比)",blank=True, null=True)
    rd_cnc = models.FloatField("读并发数",blank=True, null=True)
    rd_rt = models.FloatField("读响应时间",blank=True, null=True)
    wr_s = models.FloatField("每秒写请求数",blank=True, null=True)
    wr_avgkb = models.FloatField("写请求平均大小",blank=True, null=True)
    wr_m_s = models.FloatField("每秒写大小(mb)",blank=True, null=True)
    wr_mrg_s = models.FloatField("每秒写合并(百分比)",blank=True, null=True)
    wr_cnc = models.FloatField("写并发数",blank=True, null=True)
    wr_rt = models.FloatField("写相应时间",blank=True, null=True)
    busy = models.FloatField("%util",blank=True, null=True)
    in_prg = models.FloatField("排队请求数",blank=True, null=True)
    io_s = models.FloatField("物理磁盘吞吐量",blank=True, null=True)
    qtime = models.FloatField("IO请求队列时间(平均排队时间)",blank=True, null=True)
    stime = models.FloatField("IO请求服务时间",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_io_stat_his'
        verbose_name = "Linux磁盘IO信息"
        verbose_name_plural = verbose_name

# encoding:utf-8
from django.db import models
from django.utils import timezone

class OracleStat(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    hostname = models.CharField("主机名",max_length=255,blank=True,null=True)
    platform = models.CharField("主机平台",max_length=255,blank=True,null=True)
    num_cpus = models.IntegerField("CPU核心数",blank=True,null=True)
    physical_memory = models.FloatField("物理内存大小",blank=True,null=True)
    inst_id = models.IntegerField("实例编号",blank=True,null=True)
    instance_name = models.CharField("实例名",max_length=32,blank=True, null=True)
    db_version = models.CharField("数据库版本",max_length=32,blank=True, null=True)
    dbid = models.CharField("DBID",max_length=32,blank=True, null=True)
    created = models.DateTimeField("实例创建时间",blank=True, null=True)
    dbname = models.CharField("数据库名",max_length=32,blank=True, null=True)
    db_unique_name = models.CharField("唯一数据库名",max_length=32,blank=True, null=True)
    database_role = models.CharField("数据库角色",max_length=32,blank=True, null=True)
    open_mode = models.CharField("开启模式",max_length=32,blank=True, null=True)
    updays = models.IntegerField("启动天数",blank=True,null=True)
    audit_trail = models.CharField("审计级别",max_length=32,blank=True, null=True)
    log_mode = models.CharField("归档模式",max_length=32,blank=True, null=True)
    is_rac = models.CharField("是否为rac",max_length=8,blank=True, null=True)
    undo_tablespace = models.CharField("默认undo表空间",max_length=255,blank=True, null=True)
    flashback_on = models.CharField("是否开启闪回",max_length=8,blank=True, null=True)
    datafile_size = models.FloatField("数据文件大小",blank=True,null=True)
    tempfile_size = models.FloatField("临时文件大小",blank=True,null=True)
    archivelog_size = models.FloatField("归档量",blank=True,null=True)
    archive_used_percent = models.FloatField("归档使用率",blank=True, null=True)
    max_process = models.IntegerField("最大连接数",blank=True, null=True)
    current_process = models.IntegerField("当前使用连接数",blank=True, null=True)
    process_used_percent = models.FloatField("连接数使用率",blank=True, null=True)
    pga_target_size = models.FloatField("PGA大小(MB)",blank=True, null=True)
    pga_used_size = models.FloatField("当前PGA大小(MB)",blank=True, null=True)
    pga_used_percent = models.FloatField("PGA使用率",blank=True, null=True)
    pga_size = models.FloatField("PGA使用大小",blank=True, null=True)
    sga_size = models.FloatField("SGA使用大小",blank=True, null=True)
    memory_used_percent = models.FloatField("内存使用比例(pga+sga/totalmem)",blank=True, null=True)
    logons_cumulative = models.IntegerField("每秒登录数",blank=True, null=True)
    qps = models.IntegerField("每秒查询请求数",blank=True, null=True)
    tps = models.IntegerField("每秒事务处理数",blank=True, null=True)
    exec_count = models.IntegerField("每秒执行次数",blank=True, null=True)
    user_commits = models.IntegerField("每秒提交数",blank=True, null=True)
    user_rollbacks = models.IntegerField("每秒回滚数",blank=True, null=True)
    consistent_gets = models.IntegerField("每秒一致性读次数",blank=True, null=True)
    logical_reads = models.IntegerField("每秒逻辑读次数",blank=True, null=True)
    physical_reads = models.IntegerField("每秒物理读次数",blank=True, null=True)
    physical_writes = models.IntegerField("每秒物理写次数",blank=True, null=True)
    block_changes = models.IntegerField("每秒数据块变化数",blank=True, null=True)
    redo_size = models.FloatField("每秒写入redo buffer大小",blank=True, null=True)
    redo_writes = models.IntegerField("每秒写入redo buffer次数",blank=True, null=True)
    total_parse_count = models.IntegerField("每秒解析次数",blank=True, null=True)
    hard_parse_count = models.IntegerField("每秒硬解析次数",blank=True, null=True)
    bytes_received = models.FloatField("每秒接收数量(KB)",blank=True, null=True)
    bytes_sent = models.FloatField("每秒发送字数量(KB)",blank=True, null=True)
    io_throughput = models.FloatField("每秒发生IO数量(KB),物理读+物理写",blank=True, null=True)
    total_sessions = models.IntegerField("总会话数",blank=True, null=True)
    active_sessions = models.IntegerField("活动会话数",blank=True, null=True)
    active_trans_sessions = models.IntegerField("处理事务会话数",blank=True, null=True)
    blocked_sessions = models.IntegerField("阻塞会话数",blank=True, null=True)
    dbtime = models.FloatField(blank=True, null=True)
    dbcpu = models.FloatField(blank=True, null=True)
    log_parallel_write_wait = models.FloatField("log file parallel write平均等待时间",blank=True, null=True)
    log_file_sync_wait = models.FloatField("log file sync平均等待时间",blank=True, null=True)
    log_file_sync_count = models.IntegerField("log file sync等待次数",blank=True, null=True)
    db_file_scattered_read_wait = models.FloatField("db file scattered read平均等待时间",blank=True, null=True)
    db_file_scattered_read_count = models.IntegerField("db file scattered read等待次数",blank=True, null=True)
    db_file_sequential_read_wait = models.FloatField("db file sequential read平均等待时间",blank=True, null=True)
    db_file_sequential_read_count = models.IntegerField("db file sequential read等待次数",blank=True, null=True)
    row_lock_wait_count = models.IntegerField("enq: TX - row lock contention等待次数",blank=True, null=True)
    enq_tx_row_lock_contention = models.IntegerField("enq: TX - row lock contention等待数量",blank=True, null=True)
    enq_tm_contention = models.IntegerField("enq: TM - contentionn等待数量",blank=True, null=True)
    row_cache_lock = models.IntegerField("row cache lock等待数量",blank=True, null=True)
    library_cache_lock = models.IntegerField("library cache lock等待数量",blank=True, null=True)
    enq_tx_contention = models.IntegerField("enq: TX - contention等待数量",blank=True, null=True)
    lock_wait_others = models.IntegerField("其他等待数量",blank=True, null=True)
    adg_trans_lag = models.CharField("adg传输延迟",max_length=255,blank=True,null=True)
    adg_apply_lag = models.CharField("adg应用延迟",max_length=255,blank=True,null=True)
    adg_trans_value = models.IntegerField("adg传输延迟(秒)",blank=True, null=True)
    adg_apply_value = models.IntegerField("adg应用延迟(秒)",blank=True, null=True)
    alert_log = models.TextField("alert日志内容",blank=True,null=True)
    status = models.IntegerField("数据库连接状态 0成功 1失败",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_stat'
        verbose_name = "Oracle数据库采集数据"
        verbose_name_plural = verbose_name


class OracleTableSpace(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    tablespace_name = models.CharField("表空间名",max_length=255,blank=True,null=True)
    datafile_count = models.IntegerField("数据文件数量",blank=True, null=True)
    total_size = models.FloatField("表空间大小",blank=True, null=True)
    free_size = models.FloatField("剩余空间",blank=True, null=True)
    used_size = models.FloatField("使用空间",blank=True, null=True)
    max_free_size = models.FloatField("最大剩余空间",blank=True, null=True)
    percent_used = models.FloatField("使用百分比",blank=True, null=True)
    percent_free = models.FloatField("剩余百分比",blank=True, null=True)
    used_mb = models.FloatField("每天使用表空间大小",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_tablespace'
        verbose_name = "oracle表空间采集数据"
        verbose_name_plural = verbose_name

class OracleTempTableSpace(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    temptablespace_name = models.CharField("临时表空间名",max_length=255,blank=True,null=True)
    total_size = models.FloatField("临时表空间大小",blank=True, null=True)
    used_size = models.FloatField("使用空间",blank=True, null=True)
    percent_used = models.FloatField("使用百分比",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_temp_tablespace'
        verbose_name = "oracle临时表空间采集数据"
        verbose_name_plural = verbose_name

class OracleUndoTableSpace(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    undotablespace_name = models.CharField("undo表空间名",max_length=255,blank=True,null=True)
    total_size = models.FloatField("undo表空间大小",blank=True, null=True)
    used_size = models.FloatField("使用空间",blank=True, null=True)
    percent_used = models.FloatField("使用百分比",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_undo_tablespace'
        verbose_name = "oracle undo表空间采集数据"
        verbose_name_plural = verbose_name

class OracleTableStats(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    owner = models.CharField("用户名",max_length=64,blank=True,null=True)
    table_name = models.CharField("表名",max_length=255,blank=True,null=True)
    num_rows = models.IntegerField("表行数",blank=True,null=True)
    change_pct = models.FloatField("变更率",blank=True,null=True)
    last_analyzed = models.DateTimeField("最近统计信息收集时间",blank=True,null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_table_stats'
        verbose_name = "Oracle 统计信息分析"
        verbose_name_plural = verbose_name

class OracleControlFile(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    name = models.CharField("控制文件",max_length=255,blank=True,null=True)
    size = models.FloatField("控制文件大小(MB)",blank=True,null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_controlfile'
        verbose_name = "Oracle控制文件"
        verbose_name_plural = verbose_name

class OracleRedoLog(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    group_no = models.IntegerField("日志组",blank=True,null=True)
    thread_no = models.IntegerField("线程编号",blank=True,null=True)
    type = models.CharField("类型",max_length=32,blank=True,null=True)
    sequence_no = models.IntegerField("序列号",blank=True,null=True)
    size = models.FloatField("日志大小",blank=True,null=True)
    archived = models.CharField("是否归档",max_length=32,blank=True,null=True)
    status = models.CharField("状态",max_length=32,blank=True,null=True)
    member = models.CharField("日志文件",max_length=255,blank=True,null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_redolog'
        verbose_name = "oracle在线重做日志"
        verbose_name_plural = verbose_name

class OracleStatHis(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    hostname = models.CharField("主机名",max_length=255,blank=True,null=True)
    platform = models.CharField("主机平台",max_length=255,blank=True,null=True)
    num_cpus = models.IntegerField("CPU核心数",blank=True,null=True)
    physical_memory = models.FloatField("物理内存大小",blank=True,null=True)
    inst_id = models.IntegerField("实例编号",blank=True,null=True)
    instance_name = models.CharField("实例名",max_length=32,blank=True, null=True)
    db_version = models.CharField("数据库版本",max_length=32,blank=True, null=True)
    dbid = models.CharField("DBID",max_length=32,blank=True, null=True)
    created = models.DateTimeField("实例创建时间",blank=True, null=True)
    dbname = models.CharField("数据库名",max_length=32,blank=True, null=True)
    db_unique_name = models.CharField("唯一数据库名",max_length=32,blank=True, null=True)
    database_role = models.CharField("数据库角色",max_length=32,blank=True, null=True)
    open_mode = models.CharField("开启模式",max_length=32,blank=True, null=True)
    updays = models.IntegerField("启动天数",blank=True,null=True)
    audit_trail = models.CharField("审计级别",max_length=32,blank=True, null=True)
    log_mode = models.CharField("归档模式",max_length=32,blank=True, null=True)
    is_rac = models.CharField("是否为rac",max_length=8,blank=True, null=True)
    undo_tablespace = models.CharField("默认undo表空间",max_length=255,blank=True, null=True)
    flashback_on = models.CharField("是否开启闪回",max_length=8,blank=True, null=True)
    datafile_size = models.FloatField("数据文件大小",blank=True,null=True)
    tempfile_size = models.FloatField("临时文件大小",blank=True,null=True)
    archivelog_size = models.FloatField("归档量",blank=True,null=True)
    archive_used_percent = models.FloatField("归档使用率",blank=True, null=True)
    max_process = models.IntegerField("最大连接数",blank=True, null=True)
    current_process = models.IntegerField("当前使用连接数",blank=True, null=True)
    process_used_percent = models.FloatField("连接数使用率",blank=True, null=True)
    pga_target_size = models.FloatField("PGA大小(MB)",blank=True, null=True)
    pga_used_size = models.FloatField("当前PGA大小(MB)",blank=True, null=True)
    pga_used_percent = models.FloatField("PGA使用率",blank=True, null=True)
    pga_size = models.FloatField("PGA使用大小",blank=True, null=True)
    sga_size = models.FloatField("SGA使用大小",blank=True, null=True)
    memory_used_percent = models.FloatField("内存使用比例(pga+sga/totalmem)",blank=True, null=True)
    logons_cumulative = models.IntegerField("每秒登录数",blank=True, null=True)
    qps = models.IntegerField("每秒查询请求数",blank=True, null=True)
    tps = models.IntegerField("每秒事务处理数",blank=True, null=True)
    exec_count = models.IntegerField("每秒执行次数",blank=True, null=True)
    user_commits = models.IntegerField("每秒提交数",blank=True, null=True)
    user_rollbacks = models.IntegerField("每秒回滚数",blank=True, null=True)
    consistent_gets = models.IntegerField("每秒一致性读次数",blank=True, null=True)
    logical_reads = models.IntegerField("每秒逻辑读次数",blank=True, null=True)
    physical_reads = models.IntegerField("每秒物理读次数",blank=True, null=True)
    physical_writes = models.IntegerField("每秒物理写次数",blank=True, null=True)
    block_changes = models.IntegerField("每秒数据块变化数",blank=True, null=True)
    redo_size = models.FloatField("每秒写入redo buffer大小",blank=True, null=True)
    redo_writes = models.IntegerField("每秒写入redo buffer次数",blank=True, null=True)
    total_parse_count = models.IntegerField("每秒解析次数",blank=True, null=True)
    hard_parse_count = models.IntegerField("每秒硬解析次数",blank=True, null=True)
    bytes_received = models.FloatField("每秒接收数量(KB)",blank=True, null=True)
    bytes_sent = models.FloatField("每秒发送字数量(KB)",blank=True, null=True)
    io_throughput = models.FloatField("每秒发生IO数量(KB),物理读+物理写",blank=True, null=True)
    total_sessions = models.IntegerField("总会话数",blank=True, null=True)
    active_sessions = models.IntegerField("活动会话数",blank=True, null=True)
    active_trans_sessions = models.IntegerField("处理事务会话数",blank=True, null=True)
    blocked_sessions = models.IntegerField("阻塞会话数",blank=True, null=True)
    dbtime = models.FloatField(blank=True, null=True)
    dbcpu = models.FloatField(blank=True, null=True)
    log_parallel_write_wait = models.FloatField("log file parallel write平均等待时间",blank=True, null=True)
    log_file_sync_wait = models.FloatField("log file sync平均等待时间",blank=True, null=True)
    log_file_sync_count = models.IntegerField("log file sync等待次数",blank=True, null=True)
    db_file_scattered_read_wait = models.FloatField("db file scattered read平均等待时间",blank=True, null=True)
    db_file_scattered_read_count = models.IntegerField("db file scattered read等待次数",blank=True, null=True)
    db_file_sequential_read_wait = models.FloatField("db file sequential read平均等待时间",blank=True, null=True)
    db_file_sequential_read_count = models.IntegerField("db file sequential read等待次数",blank=True, null=True)
    row_lock_wait_count = models.IntegerField("enq: TX - row lock contention等待次数",blank=True, null=True)
    enq_tx_row_lock_contention = models.IntegerField("enq: TX - row lock contention等待数量",blank=True, null=True)
    enq_tm_contention = models.IntegerField("enq: TM - contentionn等待数量",blank=True, null=True)
    row_cache_lock = models.IntegerField("row cache lock等待数量",blank=True, null=True)
    library_cache_lock = models.IntegerField("library cache lock等待数量",blank=True, null=True)
    enq_tx_contention = models.IntegerField("enq: TX - contention等待数量",blank=True, null=True)
    lock_wait_others = models.IntegerField("其他等待数量",blank=True, null=True)
    adg_trans_lag = models.CharField("adg传输延迟",max_length=255,blank=True,null=True)
    adg_apply_lag = models.CharField("adg应用延迟",max_length=255,blank=True,null=True)
    adg_trans_value = models.IntegerField("adg传输延迟(秒)",blank=True, null=True)
    adg_apply_value = models.IntegerField("adg应用延迟(秒)",blank=True, null=True)
    alert_log = models.TextField("alert日志内容",blank=True,null=True)
    status = models.IntegerField("数据库连接状态 0成功 1失败",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_stat_his'
        verbose_name = "Oracle数据库采集数据"
        verbose_name_plural = verbose_name


class OracleTableSpaceHis(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    tablespace_name = models.CharField("表空间名",max_length=255,blank=True,null=True)
    datafile_count = models.IntegerField("数据文件数量",blank=True, null=True)
    total_size = models.FloatField("表空间大小",blank=True, null=True)
    free_size = models.FloatField("剩余空间",blank=True, null=True)
    used_size = models.FloatField("使用空间",blank=True, null=True)
    max_free_size = models.FloatField("最大剩余空间",blank=True, null=True)
    percent_used = models.FloatField("使用百分比",blank=True, null=True)
    percent_free = models.FloatField("剩余百分比",blank=True, null=True)
    used_mb = models.FloatField("每天使用表空间大小",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_tablespace_his'
        verbose_name = "oracle表空间采集数据"
        verbose_name_plural = verbose_name

class OracleTempTableSpaceHis(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    temptablespace_name = models.CharField("临时表空间名",max_length=255,blank=True,null=True)
    total_size = models.FloatField("临时表空间大小",blank=True, null=True)
    used_size = models.FloatField("使用空间",blank=True, null=True)
    percent_used = models.FloatField("使用百分比",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_temp_tablespace_his'
        verbose_name = "oracle临时表空间采集数据"
        verbose_name_plural = verbose_name

class OracleUndoTableSpaceHis(models.Model):
    tags = models.CharField("标签",max_length=32)
    host = models.CharField("主机ip",max_length=32)
    port = models.IntegerField("数据库端口号",default=1521)
    service_name = models.CharField("数据库服务名",max_length=255)
    undotablespace_name = models.CharField("undo表空间名",max_length=255,blank=True,null=True)
    total_size = models.FloatField("undo表空间大小",blank=True, null=True)
    used_size = models.FloatField("使用空间",blank=True, null=True)
    percent_used = models.FloatField("使用百分比",blank=True, null=True)
    check_time = models.DateTimeField("采集时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_undo_tablespace_his'
        verbose_name = "oracle undo表空间采集数据"
        verbose_name_plural = verbose_name


class OracleReport(models.Model):
    tags = models.CharField("标签",max_length=32)
    begin_time = models.CharField("报告开始时间",max_length=255)
    end_time = models.CharField("报告结束时间",max_length=255)
    report_type = models.CharField("报告类型 0:awr 1:ash 2:addm",max_length=255)
    file_path = models.CharField("文件路径",max_length=255)
    status = models.CharField("状态 0:已生成 1:正在生成 2:生成失败",max_length=255)
    create_time = models.DateTimeField("生成时间",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_report'
        verbose_name = "Oracle报告"
        verbose_name_plural = verbose_name


# encoding:utf-8

import time
import math
from utils.mysql_base import MysqlBase

# 0 for accumulate value, 1 for current value
mysql_stat_conf = {
    "Com_select"                        : 0,
    "Com_insert"                        : 0,
    "Com_update"                        : 0,
    "Com_delete"                        : 0,
    "Slow_queries"                      : 0,
    "Bytes_received"                    : 0,
    "Bytes_sent"                        : 0,
    "Open_files"                        : 0,
    "Open_tables"                       : 0,
    "Innodb_buffer_pool_reads"          : 0,
    "Innodb_buffer_pool_read_requests"  : 0,
    "Innodb_buffer_pool_write_requests" : 0,
    "Innodb_data_reads"                 : 0,
    "Innodb_data_writes"                : 0,
    "Innodb_log_writes"                 : 0,
    "Innodb_data_fsyncs"                : 0,
    "Innodb_row_lock_waits"             : 0,
    "Innodb_row_lock_time"              : 0,
    "Select_scan"                       : 0,
    "Sort_rows"                         : 0,
    "Threads_connected"                 : 1,
    "Threads_running"                   : 1,
    "Threads_created"                   : 1,
    "Threads_cached"                    : 1,
    "Uptime"                            : 1,
    "Questions"                         : 0,
    "Innodb_data_read"                  : 0,
    "Innodb_data_written"               : 0,
    "Innodb_os_log_fsyncs"              : 0,
    "Innodb_os_log_written"             : 0,
    "Innodb_rows_deleted"               : 0,
    "Innodb_rows_inserted"              : 0,
    "Innodb_rows_read"                  : 0,
    "Innodb_rows_updated"               : 0,
    "Innodb_buffer_pool_pages_free"     : 1,
    "Innodb_buffer_pool_pages_total"    : 1,
    "Innodb_buffer_pool_pages_data"     : 1,
    "Innodb_buffer_pool_pages_dirty"    : 1,
    "Innodb_buffer_pool_pages_flushed"  : 1,
    "Key_read_requests"                 : 0,
    "Key_reads"                         : 0,
    "Key_write_requests"                : 0,
    "Key_writes"                        : 0,
    "Key_blocks_unused"                 : 1,
    "Key_blocks_used"                   : 1,
    "Key_blocks_not_flushed"            : 1,
    "Created_tmp_disk_tables"           : 0
}

field_mapping = {
    'tps':('Com_insert Com_update Com_delete', 1),
    'qps':('Com_select Com_insert Com_update Com_delete',1),
    'slow_queries':('Slow_queries',1),
    'mysql_sel':('Com_select',1),
    'mysql_ins':('Com_insert',1),
    'mysql_upd':('Com_update',1),
    'mysql_del':('Com_delete',1),
    'questions':('Questions',1),
    'bytes_received':('Bytes_received',1.0/1024),
    'bytes_sent':('Bytes_sent', 1.0/1024),
    'innodb_buffer_pool_reads':('Innodb_buffer_pool_reads',1),
    'innodb_buffer_pool_read_requests':('Innodb_buffer_pool_read_requests',1),
    'innodb_data_reads':('Innodb_data_reads',1),
    'innodb_data_writes':('Innodb_data_writes',1),
    'innodb_data_fsyncs':('Innodb_data_fsyncs',1),
    'innodb_log_writes':('Innodb_log_writes',1),
    'innodb_row_lock_waits':('Innodb_row_lock_waits',1),
    'innodb_row_lock_time_avg':('Innodb_row_lock_time',1),
    'innodb_data_read':('Innodb_data_read',1.0/1024),
    'innodb_data_written':('Innodb_data_written',1.0/1024),
    'innodb_os_log_fsyncs':('Innodb_os_log_fsyncs',1),
    'innodb_os_log_written':('Innodb_os_log_written',1.0/1024),
    'innodb_rows_deleted':('Innodb_rows_deleted',1),
    'innodb_rows_inserted':('Innodb_rows_inserted',1),
    'innodb_rows_read':('Innodb_rows_read',1),
    'innodb_rows_updated':('Innodb_rows_updated',1),
    'select_scan':('Select_scan',1),
    'sort_rows':('Sort_rows',1),
    'open_files':('Open_files',1),
    'open_tables':('Open_tables',1),
    'threads_connected':('Threads_connected',1),
    'threads_running':('Threads_running',1),
    'threads_created': ('Threads_created', 1),
    'threads_cached': ('Threads_cached', 1),
    'uptime': ('Uptime', 1),
    'innodb_buffer_pool_pages_total':('Innodb_buffer_pool_pages_total',1),
    'innodb_buffer_pool_pages_data': ('Innodb_buffer_pool_pages_data', 1),
    'innodb_buffer_pool_pages_dirty': ('Innodb_buffer_pool_pages_dirty', 1),
    'innodb_buffer_pool_pages_flushed': ('Innodb_buffer_pool_pages_flushed', 1),
    'innodb_buffer_pool_pages_free':('Innodb_buffer_pool_pages_free',1),
    'key_read_requests':('Key_read_requests',1),
    'key_reads':('Key_reads',1),
    'key_write_requests':('Key_write_requests',1),
    'Key_writes':('Key_writes',1),
    'key_blocks_unused':('Key_blocks_unused',1),
    'key_blocks_used':('Key_blocks_used',1),
    'key_blocks_not_flushed': ('Key_blocks_not_flushed', 1),
    'disk_tmp_tabs': ('Created_tmp_disk_tables', 1)
}


class MySQLStat(MysqlBase):
    def __init__(self,params,db_conn):
        super().__init__(params)
        self.db_conn = db_conn
        self.stat = {}
        self.stat1 = {}
        self.stat2 = {}
        self.stat_now = {}
        self.loop_cnt = 0
        self.last_time = time.time()

    def init_stat_vals(self):
        stat_dict = {}
        for var_name in mysql_stat_conf:
            stat_dict[var_name] = 0

        self.stat1['mysqlstat'] = stat_dict

    def get_mysql_stat(self):
        stat2_dict = {}
        stat_now = {}
        old_stat = self.stat1['mysqlstat']

        sql  = "show global status"
        ret = super().query(sql,self.db_conn)

        for var_name, value in ret:
            if var_name in mysql_stat_conf:
                stat2_dict[var_name] = float(value)

        # get elapsed
        if self.loop_cnt == 0:
            elapsed = stat2_dict['Uptime']
        else:
            elapsed = time.time() - self.last_time

        self.last_time = time.time()
        self.loop_cnt += 1

        for var_name in stat2_dict:
            if mysql_stat_conf[var_name] == 0:
                stat_now[var_name] = round(1.0 * (stat2_dict[var_name] - old_stat[var_name]) / elapsed, 2)
            else:
                stat_now[var_name] = stat2_dict[var_name]

        self.stat['mysqlstat'] = stat_now
        self.stat1['mysqlstat'] = stat2_dict

        return stat_now

    def format_stat(self):
        stat_columns = []
        stat_values = []
        stat_now = self.stat['mysqlstat']
        for field in sorted(field_mapping.keys()):
            stat_columns.append(field)
            stat_value = 0
            field_cols, scale_factor = field_mapping[field]
            for ff in field_cols.split():
                stat_value += stat_now[ff]
            stat_values.append(stat_value * scale_factor)

        res = dict(zip(stat_columns,stat_values))

        return res

    def get_mysql_params(self):
        sql = """
        show global variables where variable_name in (
                'innodb_buffer_pool_size',
                'max_connections',
                'max_connect_errors',
                'max_user_connections',
                'enforce_gtid_consistency',
                'gtid_mode',
                'gtid_next',
                'gtid_owned',
                'gtid_executed',
                'gtid_purged',
                'master-info-repository',
                'relay-log-info-repository',
                'sync_master_info',
                'version',
                'datadir',
                'basedir',
                'slow_query_log',
                'slow_query_log_file',
                'log_bin',
                'open_files_limit',
                'table_open_cache',
                'key_buffer_size',
                'sort_buffer_size',
                'join_buffer_size',
                'innodb_io_capacity',
                'innodb_read_io_threads',
                'innodb_write_io_threads'
        )
        """
        params = super().query(sql,self.db_conn)

        param_dict = {}
        for param_name, param_value in params:
            param_dict[param_name] = param_value

        return param_dict

    def get_threads_waited(self):
        sql = "select count(1) from information_schema.processlist where state <> '' and user <> 'repl' and time > 2"
        res = super().query(sql)
        return res[0][0]

    def get_totalsize(self):
        sql = " select sum(table_rows) as '记录数',sum(truncate(data_length / 1024 / 1024 / 1024, 2)) as '数据容量(GB)',sum(truncate(index_length / 1024 / 1024 / 1024, 2)) as '索引容量(GB)' from information_schema.tables "
        res = super().query(sql)
        return res[0]

if __name__ =='__main__':
    mysql_params = {
        'host' : '192.168.48.50',
        'port':3306,
        'user':'root',
        'password':'mysqld'
    }
    db_conn = MysqlBase(mysql_params).connection()
    mysqlstat= MySQLStat(mysql_params,db_conn)
    mysqlstat.init_stat_vals()
    mysqlstat.get_mysql_stat()
    time.sleep(1)
    mysqldata = mysqlstat.get_mysql_stat()
    print(mysqlstat.format_stat())
    mysqlparams = mysqlstat.get_mysql_params()
    print(mysqlparams)

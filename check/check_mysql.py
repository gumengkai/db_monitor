# encoding:utf-8

from utils.tools import mysql_exec,now,clear_table,archive_table
import check.checklog as checklog
from utils.mysql_base import MysqlBase
from check.mysql_stat import MySQLStat
from check.mysql_logparser import get_mysql_alert
from check.mysql_slowqueryparse import get_mysql_slowquery
import time
import timeout_decorator

@timeout_decorator.timeout(60)
def check_mysql(tags, mysql_params):
    check_time = now()
    host = mysql_params['host']
    port = mysql_params['port']
    linux_params = {
        'hostname': mysql_params['host'],
        'port': mysql_params['sshport_os'],
        'username': mysql_params['user_os'],
        'password': mysql_params['password_os']
    }
    # create connection
    mysql_conn = MysqlBase(mysql_params).connection()

    if mysql_conn:
        checklog.logger.info('{}:开始获取MySQL数据库监控信息' .format(tags))
        # get mysqlstat data
        mysqlstat = MySQLStat(mysql_params, mysql_conn)
        mysqlstat.init_stat_vals()
        mysqlstat.get_mysql_stat()
        time.sleep(1)
        mysqlstat.get_mysql_stat()
        mysqldata = mysqlstat.format_stat()
        # get mysql params
        mysqlparams = mysqlstat.get_mysql_params()
        #
        updays = round(float(mysqldata['uptime'])/86400,2)
        threads_waited = mysqlstat.get_threads_waited()
        total_rows,data_size,index_size = mysqlstat.get_totalsize()
        innodb_buffer_pool_read_requests = mysqldata['innodb_buffer_pool_read_requests']
        innodb_buffer_pool_reads = mysqldata['innodb_buffer_pool_reads']
        innodb_buffer_pool_hit = (1 - innodb_buffer_pool_reads / innodb_buffer_pool_read_requests) * 100 if innodb_buffer_pool_read_requests != 0 else 100

        checklog.logger.info('{}：写入mysql_stat采集数据' .format(tags))
        clear_table(tags,'mysql_stat')

        insert_data_sql = "insert into mysql_stat(tags,host,port,version,updays,basedir,datadir,slow_query_log,slow_query_log_file,log_bin," \
                          "max_connections,max_connect_errors,total_rows,data_size,index_size,threads_connected,threads_running,threads_waited,threads_created,threads_cached," \
                          "qps,tps,bytes_received,bytes_sent,open_files_limit,open_files,table_open_cache,open_tables,key_buffer_size,sort_buffer_size,join_buffer_size," \
                          "key_blocks_unused,key_blocks_used,key_blocks_not_flushed,mysql_sel,mysql_ins,mysql_upd,mysql_del,select_scan,slow_queries," \
                          "key_read_requests,key_reads,key_write_requests,Key_writes,innodb_buffer_pool_size,innodb_buffer_pool_pages_total,innodb_buffer_pool_pages_data," \
                          "innodb_buffer_pool_pages_dirty,innodb_buffer_pool_pages_free,innodb_buffer_pool_hit,innodb_io_capacity," \
                          "innodb_read_io_threads,innodb_write_io_threads,innodb_rows_deleted,innodb_rows_inserted,innodb_rows_read,innodb_rows_updated," \
                          "innodb_row_lock_waits,innodb_row_lock_time_avg,innodb_buffer_pool_pages_flushed,innodb_data_read,innodb_data_written,innodb_data_reads," \
                          "innodb_data_writes,innodb_log_writes,innodb_data_fsyncs,innodb_os_log_written,status,check_time) " \
                          "values ('{tags}','{host}','{port}','{version}','{updays}','{basedir}','{datadir}','{slow_query_log}','{slow_query_log_file}','{log_bin}'," \
                          "{max_connections},{max_connect_errors},{total_rows},{data_size},{index_size},{threads_connected},{threads_running},{threads_waited},{threads_created},{threads_cached}," \
                          "{qps},{tps},{bytes_received},{bytes_sent},{open_files_limit},{open_files},{table_open_cache},{open_tables},{key_buffer_size},{sort_buffer_size},{join_buffer_size}," \
                          "{key_blocks_unused},{key_blocks_used},{key_blocks_not_flushed},{mysql_sel},{mysql_ins},{mysql_upd},{mysql_del},{select_scan},{slow_queries}," \
                          "{key_read_requests},{key_reads},{key_write_requests},{Key_writes},{innodb_buffer_pool_size},{innodb_buffer_pool_pages_total},{innodb_buffer_pool_pages_data}," \
                          "{innodb_buffer_pool_pages_dirty},{innodb_buffer_pool_pages_free},{innodb_buffer_pool_hit},{innodb_io_capacity}," \
                          "{innodb_read_io_threads},{innodb_write_io_threads},{innodb_rows_deleted},{innodb_rows_inserted},{innodb_rows_read},{innodb_rows_updated}," \
                          "{innodb_row_lock_waits},{innodb_row_lock_time_avg},{innodb_buffer_pool_pages_flushed},{innodb_data_read},{innodb_data_written},{innodb_data_reads}," \
                          "{innodb_data_writes},{innodb_log_writes},{innodb_data_fsyncs},{innodb_os_log_written},0,'{check_time}' )"

        insert_data_values = {**mysqldata,**mysqlparams,**locals()}
        insert_sql = insert_data_sql.format(**insert_data_values)
        mysql_exec(insert_sql)
        archive_table(tags,'mysql_stat')

        # 后台日志解析
        get_mysql_alert(tags,mysql_params,linux_params)

        # 慢查询日志解析
        get_mysql_slowquery(tags,mysql_params,linux_params)
    else:
        error_msg = "{}:mysql数据库连接失败".format(tags)
        checklog.logger.error(error_msg)
        checklog.logger.info('{}:写入mysql_stat采集数据'.format(tags))
        clear_table(tags, 'mysql_stat')
        sql = "insert into mysql_stat(tags,host,port,status,check_time) values('{tags}','{host}',{port},1,'{check_time}')"
        sql = sql.format(**locals())
        mysql_exec(sql)
        archive_table(tags, 'mysql_stat')


if __name__ =='__main__':
    mysql_params = {
        'host' : '192.168.48.50',
        'port':3306,
        'user':'root',
        'password':'mysqld'
    }
    check_mysql('mysql50',mysql_params)

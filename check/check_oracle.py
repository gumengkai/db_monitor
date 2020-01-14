# encoding:utf-8

import check.checklog as checklog
from .oracle_info import *
from utils.oracle_base import OracleBase
from check.oracle_stat import OracleStat
from utils.tools import mysql_exec,now,clear_table,archive_table
from check.oracle_logparser import get_oracle_alert
import time
from datetime import datetime

def check_oracle(tags,oracle_params):
    db_version = oracle_params['db_version']
    host = oracle_params['host']
    port = oracle_params['port']
    service_name = oracle_params['service_name']
    linux_params = {
        'hostname': oracle_params['host'],
        'port': oracle_params['sshport_os'],
        'username': oracle_params['user_os'],
        'password': oracle_params['password_os']
    }
    check_time = now()
    db_conn = OracleBase(oracle_params).connection()
    db_conn_cdb = OracleBase(oracle_params).connection_cdb() if db_version == 'Oracle12c' else db_conn

    if db_conn and db_conn_cdb:
        # db信息监控
        checklog.logger.info('{}:开始获取Oracle数据库监控信息' .format(tags))
        # 数据库
        dbname, db_unique_name, database_role, open_mode, log_mode, dbid, flashback_on, platform, created = database_info(db_conn)
        # 容量
        datafile_size = round(get_datafile_size(db_conn)[0],2)
        tempfile_size = round(get_tempfile_size(db_conn)[0],2)
        archivelog_size = round(get_archivelog_size(db_conn)[0],2)
        # 实例
        inst_id, instance_name, hostname, startup_time, version = instance_info(db_conn)
        updays = (datetime.now() - startup_time).days
        # 连接数
        max_process,current_process,process_used_percent = process_info(db_conn_cdb)
        # 归档
        archive_used_percent = get_archived(db_conn)
        # 审计
        audit_trail = para(db_conn,'audit_trail')
        is_rac = para(db_conn,'cluster_database')
        # 默认Undo表空间
        undo_tablespace = para(db_conn,'undo_tablespace')
        # Oraclestat
        oraclestat = OracleStat(oracle_params,db_conn)
        oraclestat.get_oracle_stat()
        time.sleep(1)
        oracle_data = oraclestat.get_oracle_stat()
        # 状态数据
        oracle_osstat = oracle_data['os']
        oracle_stat = oracle_data['stat']
        oracle_wait = oracle_data['wait']
        oracle_sess = oracle_data['sess']
        oracle_mem = oracle_data['mem']
        oracle_load = oracle_data['load']
        # PGA使用率
        pga_target_size,pga_used_size,pga_used_percent = pga(db_conn)
        if database_role == 'PYSICAL STANDBY DATABASE':
            adg_trans_lag, adg_trans_value = adg_trans(db_conn)
            adg_apply_lag, adg_apply_value = adg_apply(db_conn)
        else:
            adg_trans_lag = 'None'
            adg_apply_lag = 'None'
            adg_trans_value = 0
            adg_apply_value = 0

        # 锁等待信息
        lock_wait_res = get_lockwait_count(db_conn)
        dic_lock_wait = {each[0]: each[1] for each in lock_wait_res}
        enq_tx_row_lock_contention = dic_lock_wait.get('enq: TX - row lock contention', 0)
        enq_tm_contention = dic_lock_wait.get('enq: TM - contention', 0)
        row_cache_lock = dic_lock_wait.get('row cache lock', 0)
        library_cache_lock = dic_lock_wait.get('library cache lock', 0)
        enq_tx_contention = dic_lock_wait.get('enq: TX - contention', 0)
        lock_wait_others = sum(each[1] for each in lock_wait_res) - (
                    enq_tx_row_lock_contention + enq_tm_contention + row_cache_lock + library_cache_lock + enq_tx_contention)

        checklog.logger.info('{}：写入oracle_stat采集数据' .format(tags))
        clear_table(tags,'oracle_stat')

        insert_data_values = {**locals(),**oracle_osstat,**oracle_wait,**oracle_load,**oracle_sess,**oracle_stat,**oracle_mem}

        insert_data_sql = "insert into oracle_stat(tags,host,port,service_name,hostname,platform,num_cpus,physical_memory,inst_id,instance_name,db_version," \
                          "dbid,created,dbname,db_unique_name,database_role,open_mode,updays,audit_trail,log_mode,is_rac,undo_tablespace,flashback_on," \
                          "datafile_size,tempfile_size,archivelog_size," \
                          "archive_used_percent,max_process,current_process,process_used_percent,pga_target_size,pga_used_size," \
                          "pga_used_percent,pga_size,sga_size,memory_used_percent,logons_cumulative,qps,tps,exec_count,user_commits,user_rollbacks," \
                          "consistent_gets,logical_reads,physical_reads,physical_writes,block_changes,redo_size,redo_writes,total_parse_count," \
                          "hard_parse_count,bytes_received,bytes_sent,io_throughput,total_sessions,active_sessions,active_trans_sessions," \
                          "blocked_sessions,dbtime,dbcpu,log_parallel_write_wait,log_file_sync_wait,log_file_sync_count," \
                          "db_file_scattered_read_wait,db_file_scattered_read_count,db_file_sequential_read_wait,db_file_sequential_read_count," \
                          "row_lock_wait_count,enq_tx_row_lock_contention,enq_tm_contention,row_cache_lock,library_cache_lock,enq_tx_contention,lock_wait_others," \
                          "adg_trans_lag,adg_apply_lag,adg_trans_value,adg_apply_value,status,check_time) " \
                          "values('{tags}','{host}',{port},'{service_name}','{hostname}','{platform}',{num_cpus},{physical_memory},{inst_id},'{instance_name}','{version}'," \
                          "{dbid},'{created}','{dbname}','{db_unique_name}','{database_role}','{open_mode}',{updays},'{audit_trail}','{log_mode}','{is_rac}','{undo_tablespace}','{flashback_on}'," \
                          "{datafile_size},{tempfile_size},{archivelog_size}," \
                          "{archive_used_percent},{max_process},{current_process},{process_used_percent},{pga_target_size},{pga_used_size}," \
                          "{pga_used_percent},{pga_size},{sga_size},{memory_used_percent},{logons_cumulative},{qps},{tps},{exec_count},{user_commits},{user_rollbacks}," \
                          "{consistent_gets},{logical_reads},{physical_reads},{physical_writes},{block_changes},{redo_size},{redo_writes},{total_parse_count}," \
                          "{hard_parse_count},{bytes_received},{bytes_sent},{io_throughput},{total_sessions},{active_sessions},{active_trans_sessions}," \
                          "{blocked_sessions},{dbtime},{dbcpu},{log_parallel_write_wait},{log_file_sync_wait},{log_file_sync_count}," \
                          "{db_file_scattered_read_wait},{db_file_scattered_read_count},{db_file_sequential_read_wait},{db_file_sequential_read_count}," \
                          "{row_lock_wait_count},{enq_tx_row_lock_contention},{enq_tm_contention},{row_cache_lock},{library_cache_lock},{enq_tx_contention},{lock_wait_others}," \
                          "'{adg_trans_lag}','{adg_apply_lag}',{adg_trans_value},{adg_apply_value},0,'{check_time}' )"

        insert_sql = insert_data_sql.format(**insert_data_values)
        mysql_exec(insert_sql)
        checklog.logger.info('{}：获取Oracle数据库监控数据(数据库名：{} 数据库角色：{} 数据库状态：{})' .format(tags, dbname, database_role, open_mode))
        archive_table(tags,'oracle_stat')

        # control file
        clear_table(tags, 'oracle_controlfile')
        controlfile_list = get_controlfile(db_conn)
        for each in controlfile_list:
            control_name,size = each
            insert_data_sql = "insert into oracle_controlfile(tags,host,port,service_name,name,size,check_time)" \
                              "values('{tags}','{host}',{port},'{service_name}','{control_name}',{size},'{check_time}')"
            insert_sql = insert_data_sql.format(**locals())
            mysql_exec(insert_sql)

        # redolog
        clear_table(tags, 'oracle_redolog')
        redolog_list = get_redolog(db_conn)
        for each in redolog_list:
            group_no,thread_no,type,sequence_no,size,archived,status,member = each
            insert_data_sql = "insert into oracle_redolog(tags,host,port,service_name,group_no,thread_no,type,sequence_no," \
                              "size,archived,status,member,check_time)" \
                                  "values('{tags}','{host}',{port},'{service_name}',{group_no},{thread_no},'{type}',{sequence_no}," \
                              "{size},'{archived}','{status}','{member}','{check_time}')"
            insert_sql = insert_data_sql.format(**locals())
            mysql_exec(insert_sql)

        # 表空间
        clear_table(tags, 'oracle_tablespace')
        tbsinfo_list = tablespace(db_conn)
        for tbsinfo in tbsinfo_list:
            tablespace_name,datafile_count,total_size,free_size,used_size,max_free_size,percent_used,percent_free,used_mb = tbsinfo
            insert_data_sql = "insert into oracle_tablespace(tags,host,port,service_name,tablespace_name,datafile_count,total_size,free_size," \
                              "used_size,max_free_size,percent_used,percent_free,used_mb,check_time)" \
                              "values('{tags}','{host}',{port},'{service_name}','{tablespace_name}',{datafile_count},{total_size},{free_size}," \
                              "{used_size},{max_free_size},{percent_used},{percent_free},{used_mb},'{check_time}')"
            insert_sql = insert_data_sql.format(**locals())
            mysql_exec(insert_sql)
        archive_table(tags, 'oracle_tablespace')

        # 临时表空间
        clear_table(tags, 'oracle_temp_tablespace')
        temptbsinfo_list = temp_tablespace(db_conn)
        for temptbsinfo in temptbsinfo_list:
            temptablespace_name, total_size, used_size, percent_used = temptbsinfo
            insert_data_sql = "insert into oracle_temp_tablespace(tags,host,port,service_name,temptablespace_name,total_size,used_size," \
                              "percent_used,check_time)" \
                              "values('{tags}','{host}',{port},'{service_name}','{temptablespace_name}',{total_size}," \
                              "{used_size},{percent_used},'{check_time}')"
            insert_sql = insert_data_sql.format(**locals())
            mysql_exec(insert_sql)
        archive_table(tags, 'oracle_temp_tablespace')

         # undo表空间
        clear_table(tags, 'oracle_undo_tablespace')
        undotbsinfo_list = get_undo_tablespace(db_conn)
        for undotbsinfo in undotbsinfo_list:
            undotablespace_name, total_size, used_size, percent_used = undotbsinfo
            insert_data_sql = "insert into oracle_undo_tablespace(tags,host,port,service_name,undotablespace_name,total_size,used_size," \
                              "percent_used,check_time)" \
                              "values('{tags}','{host}',{port},'{service_name}','{undotablespace_name}',{total_size}," \
                              "{used_size},{percent_used},'{check_time}')"
            insert_sql = insert_data_sql.format(**locals())
            mysql_exec(insert_sql)
        archive_table(tags, 'oracle_undo_tablespace')

        # 统计信息分析
        clear_table(tags,'oracle_table_stats')
        oracletablestats_list = get_tab_stats(db_conn)
        for each in oracletablestats_list:
            owner,table_name,num_rows,change_pct,last_analyzed = each
            insert_data_sql = "insert into oracle_table_stats(tags,host,port,service_name,owner,table_name,num_rows,change_pct,last_analyzed,check_time) " \
                              "values('{tags}','{host}',{port},'{service_name}','{owner}','{table_name}',{num_rows},{change_pct},'{last_analyzed}','{check_time}')"
            insert_sql = insert_data_sql.format(**locals())
            mysql_exec(insert_sql)

        # 后台日志解析
        get_oracle_alert(tags,db_conn,oracle_params,linux_params)

        db_conn.close()
    else:
        error_msg = "{}:数据库连接失败" .format(tags)
        checklog.logger.error(error_msg)
        clear_table(tags,'oracle_stat')
        checklog.logger.info('{}:写入oracle_stat采集数据'.format(tags))
        sql = "insert into oracle_stat(tags,host,port,service_name,status,check_time) values(%s,%s,%s,%s,%s,%s)"
        value = (tags, oracle_params['host'], oracle_params['port'], oracle_params['service_name'], 1,check_time)
        mysql_exec(sql, value)
        archive_table(tags,'oracle_stat')

# encoding;utf-8

from utils.oracle_base import *

# 获取dbinfo,name,database_role,open_mode
def database_info(db_conn):
    sql = "select name,db_unique_name,database_role,open_mode,log_mode,dbid,flashback_on,platform_name,created from v$database"
    return query_one(db_conn,sql)

# 获取实例信息
def instance_info(db_conn):
    sql = "select instance_number,instance_name,host_name,startup_time,version from v$instance"
    return query_one(db_conn,sql)

# 获取密码过期信息
def pwd_info(db_conn):
    sql = ''' select username, trunc(expiry_date - sysdate) result_number
  from dba_users
 where expiry_date is not null
   and account_status = 'OPEN'
   and expiry_date - sysdate <  7
   and username not in ('SYS')
 '''
    return query_all(db_conn,sql)

# 获取归档使用情况
def get_archived(db_conn):
    sql = ''' select percent_space_used from v$flash_recovery_area_usage a where a.file_type='ARCHIVED LOG' '''
    res =  query_one(db_conn,sql)
    return res[0] if res else 0

# 获取等待事件信息
def wait_events(db_conn):
    sql = '''select event#, event, count(*) from v$session group by event#, event order by 3'''
    return query_all(db_conn,sql)

# 获取无效索引
def invalid_index(db_conn):
    sql = '''select owner, index_name, '' partition_name, status
  from dba_indexes
 where status not in ('VALID', 'N/A')
union all
select i.owner, i.index_name, p.partition_name, p.status
  from dba_ind_partitions p, dba_indexes i
 where p.index_name = i.index_name
   and p.index_owner = i.owner
   and p.status != 'USABLE'
union all
select i.owner, i.index_name, s.subpartition_name, s.status
  from dba_ind_subpartitions s, dba_indexes i
 where s.index_name = i.index_name
   and s.index_name = i.index_name
   and s.status != 'USABLE' '''
    return query_all(db_conn,sql)


# 获取锁等待信息
def lock_info(db_conn):
    sql = '''SELECT DECODE(request, 0, 'Holder: ', 'Waiter: ') || SID sess,
       decode(lmode,
              0,
              'none',
              1,
              'null',
              2,
              'row share',
              3,
              'row exclusive',
              4,
              'share',
              5,
              'share row exclusive',
              6,
              'exclusive') lmode,
       ctime,
       inst_id,
       id1,
       id2,
       lmode,
       request,
       TYPE,
       sid session_id
  FROM gV$LOCK
 WHERE (id1, id2, TYPE) IN
       (SELECT id1, id2, TYPE FROM gV$LOCK WHERE request > 0)
 ORDER BY id1, request'''
    return query_all(db_conn,sql)

# 获取连接数信息
def process_info(db_conn):
    sql = '''select current_utilization,limit_value,trunc(current_utilization * 100 / limit_value) Result_Number
  from v$resource_limit
 where resource_name in ('processes')'''
    return query_one(db_conn,sql)

# 获取PGA使用率
def pga(db_conn):
    sql = '''select round(b.value / 1024 / 1024, 1) pga_target,
       round(a.pga_used_mb, 1),
       round(a.pga_used_mb / (b.value / 1024 / 1024), 1) * 100  pga_used_pct
  from (select sum(PGA_ALLOC_MEM) / 1024 / 1024 pga_used_mb from v$process) a,
       v$parameter b
 where b.name = 'pga_aggregate_target' '''
    return query_one(db_conn,sql)

# 获取asm存储信息
def asm(db_conn):
    sql = '''select name,state,total_mb,free_mb,usable_file_mb from v$asm_diskgroup'''
    return query_all(db_conn,sql)

# 获取adg传输延迟
def adg_trans(db_conn):
    sql = "select value,substr(value,2,2)*24*3600+substr(value,5,2)*3600+substr(value,8,2)*60+substr(value,11,2) from v$dataguard_stats where name='transport lag'"
    return query_all(db_conn,sql)

# 获取adg应用延迟
def adg_apply(db_conn):
    sql = "select value,substr(value,2,2)*24*3600+substr(value,5,2)*3600+substr(value,8,2)*60+substr(value,11,2) from v$dataguard_stats where name='apply lag'"
    return query_all(db_conn,sql)

# 获取表空间使用率
def tablespace(db_conn):
    sql = '''SELECT T1.*, T2.USED_MB
  FROM (SELECT DF.TABLESPACE_NAME,
               COUNT(*) DATAFILE_COUNT,
               ROUND(SUM(DF.BYTES) / 1048576 / 1024, 2) SIZE_GB,
               ROUND(SUM(FREE.BYTES) / 1048576 / 1024, 2) FREE_GB,
               ROUND(SUM(DF.BYTES) / 1048576 / 1024 -
                     SUM(FREE.BYTES) / 1048576 / 1024,
                     2) USED_GB,
               ROUND(MAX(FREE.MAXBYTES) / 1048576 / 1024, 2) MAXFREE,
               100 - ROUND(100.0 * SUM(FREE.BYTES) / SUM(DF.BYTES), 2) PCT_USED,
               ROUND(100.0 * SUM(FREE.BYTES) / SUM(DF.BYTES), 2) PCT_FREE
          FROM DBA_DATA_FILES DF,
               (SELECT TABLESPACE_NAME,
                       FILE_ID,
                       SUM(BYTES) BYTES,
                       MAX(BYTES) MAXBYTES
                  FROM DBA_FREE_SPACE
                 GROUP BY TABLESPACE_NAME, FILE_ID) FREE
         WHERE DF.TABLESPACE_NAME = FREE.TABLESPACE_NAME(+)
           AND DF.TABLESPACE_NAME NOT LIKE 'UNDO%'
           AND DF.FILE_ID = FREE.FILE_ID(+)
         GROUP BY DF.TABLESPACE_NAME) T1,
       (SELECT B.NAME,
               ROUND(SUM(TABLESPACE_USEDSIZE) / 1024 / 1024 / 7, 2) USED_MB
          FROM DBA_HIST_TBSPC_SPACE_USAGE A, V$TABLESPACE B
         WHERE A.TABLESPACE_ID = B.TS#
           AND TO_DATE(RTIME, 'mm/dd/yyyy hh24:mi:ss') > SYSDATE - 6
         GROUP BY B.NAME) T2
 WHERE T1.TABLESPACE_NAME = T2.NAME'''
    return query_all(db_conn,sql)

# 获取临时表空间使用率
def temp_tablespace(db_conn):
    sql = '''SELECT A.tablespace_name tablespace,
       D.mb_total,
       SUM(A.used_blocks * D.block_size) / 1024 / 1024 mb_used,
       trunc(100*SUM(A.used_blocks * D.block_size) / 1024 / 1024/D.mb_total) used_PCT
  FROM v$sort_segment A,
       (SELECT B.name, C.block_size, SUM(C.bytes) / 1024 / 1024 mb_total
          FROM v$tablespace B, v$tempfile C
         WHERE B.ts# = C.ts#
         GROUP BY B.name, C.block_size) D
 WHERE A.tablespace_name = D.name
 GROUP by A.tablespace_name, D.mb_total'''
    return query_all(db_conn,sql)

# 获取undo表空间使用率
def get_undo_tablespace(db_conn):
    sql = '''select  b.tablespace_name,
       nvl(used_undo, 0) "USED_UNDO(M)",
       total_undo "Total_undo(M)",
       trunc(nvl(used_undo, 0) / total_undo * 100, 2) used_PCT
  from (select nvl(sum(bytes / 1024 / 1024), 0) used_undo, tablespace_name
          from dba_undo_extents
         where status in ('ACTIVE', 'UNEXPIRED')
           and tablespace_name in
               (select value from v$parameter where name = 'undo_tablespace')
         group by tablespace_name) a,
       (select tablespace_name, sum(bytes / 1024 / 1024) total_undo
          from dba_data_files
         where tablespace_name in
               (select upper(value) from v$parameter where name = 'undo_tablespace')
         group by tablespace_name) b
 where a.tablespace_name(+) = b.tablespace_name'''
    return query_all(db_conn,sql)

def para(db_conn,para):
    sql = "select a.VALUE from v$parameter a where a.name='%s' " %para
    res = query_one(db_conn,sql)
    return res[0]

# 获取数据文件大小
def get_datafile_size(db_conn):
    sql = 'select sum(bytes)/1024/1024/1024 from dba_data_files'
    return query_one(db_conn,sql)

# 获取临时文件大小
def get_tempfile_size(db_conn):
    sql = 'select sum(bytes)/1024/1024/1024 from dba_temp_files'
    return query_one(db_conn,sql)

# 获取归档量
def get_archivelog_size(db_conn):
    sql = "select nvl(sum(blocks*block_size)/1024/1024/1024,0) from v$archived_log where archived='YES' and deleted='NO' "
    return query_one(db_conn,sql)

# 统计信息分析
def get_tab_stats(db_conn):
    sql = '''
    select owner,table_name,num_rows,change_pct,last_analyzed
  from (select t1.owner,
               t1.table_name,
               t1.num_rows,
               ROUND((T2.inserts + T2.updates + T2.deletes) / T1.num_rows * 100,
                     2) change_pct,
               T1.last_analyzed
          from dba_tables t1, dba_tab_modifications t2
         where t1.owner = t2.table_owner
           and t1.table_name = t2.table_name
           and t1.num_rows>0)
 where change_pct > 10
    '''
    return query_all(db_conn,sql)

# 获取controlfile信息
def get_controlfile(db_conn):
    sql = "select name,round(block_size*file_size_blks/1024/1024,2) size_M  from v$controlfile"
    return query_all(db_conn,sql)

# 获取asm存储信息
def get_redolog(db_conn):
    sql =  """select a.GROUP# group_no,b.THREAD# thread_no,a.TYPE,b.SEQUENCE# sequence_no,b.BYTES/1024/1024 SIZE_M,b.ARCHIVED,b.STATUS,a.MEMBER from v$logfile a,v$log b where a.GROUP#=b.GROUP#(+)"""
    return query_all(db_conn,sql)

# 获取锁等待信息
def get_lockwait_count(db_conn):
    sql =  "select event, count(1) cnt " \
           "from v$session " \
           "where wait_class != 'Idle' " \
           "group by event"
    return query_all(db_conn,sql)

if __name__ =='__main__':
    oracle_params = {
        'host' : '192.168.48.60',
        'port':1521,
        'service_name':'pdb1',
        'user':'dbmon',
        'password':'oracle',
        'service_name_cdb':'orcl',
        'user_cdb':'c##dbmon',
        'password_cdb':'oracle'
    }
    db_conn = OracleBase(oracle_params).connection()
    res = get_lockwait_count(db_conn)
    print(res)
    dic_res = {each[0]:each[1] for each in res}
    print(dic_res)
    enq_tx_row_lock_contention = dic_res.get('enq: TX - row lock contention',0)
    enq_tm_contention = dic_res.get('enq: TM - contention',0)
    row_cache_lock = dic_res.get('row cache lock',0)
    library_cache_lock = dic_res.get('library cache lock',0)
    enq_tx_contention = dic_res.get('enq: TX - contention',0)
    lock_wait_others = sum(each[1] for each in res) - (enq_tx_row_lock_contention+row_cache_lock+library_cache_lock+enq_tx_contention)




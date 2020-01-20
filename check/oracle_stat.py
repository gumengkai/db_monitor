# encoding:utf-8

import math
import time
import datetime
from collections import defaultdict
from utils.oracle_base import OracleBase

class OracleStat(OracleBase):
    def __init__(self,params,db_conn):
        super().__init__(params)
        self.db_conn = db_conn
        self.proc_stat = {}
        self.last_time = time.time()
        self.loop_cnt = 0
        self.stat = {}
        self.old_stat = {}
        self.ora_stats = (
            "bytes received via SQL*Net from client",
            "bytes sent via SQL*Net to client",
            "session logical reads",
            "consistent gets",
            "enqueue waits",
            "execute count",
            "leaf node splits",
            "logons cumulative",
            "parse count (total)",
            "parse count (hard)",
            "physical reads",
            "physical writes",
            "redo size",
            "sorts (memory)",
            "sorts (disk)",
            "table scans (long tables)",
            "table scans (short tables)",
            "transaction rollbacks",
            "user commits",
            "user rollbacks",
            "redo synch time",
            "redo synch writes",
            "user calls",
            "SQL*Net roundtrips to/from client",
            "gc cr blocks served",
            "gc cr blocks received",
            "gc cr block receive time",
            "gc cr block send time",
            "gc current blocks served",
            "gc current blocks received",
            "gc current block receive time",
            "gc current block send time",
            "gcs messages sent",
            "ges messages sent",
            "db block changes",
            "redo writes",
            "physical read total bytes",
            "physical write total bytes"
        )
        self.wait_events = (
            "db file sequential read",
            "db file scattered read",
            "log file parallel write",
            "log file sync",
            "log file parallel write",
            "enq: TX - row lock contention"
        )
        self.time_model = (
            'DB time',
            'DB CPU',
            'background cpu time'
        )

        self.os_stats = (
            'PHYSICAL_MEMORY_BYTES', 'NUM_CPUS', 'IDLE_TIME', 'BUSY_TIME'
        )

        self.old_stat = {}

        for stat in self.ora_stats:
            self.old_stat[stat] = 0

        for stat in self.wait_events:
            self.old_stat[stat] = 0
            self.old_stat[stat + '/time waited'] = 0

        for stat_name in self.time_model:
            self.old_stat[stat_name] = 0

        for stat_name in self.os_stats:
            self.old_stat[stat_name] = 0

    def get_uptime(self):
        sql = "select startup_time, version, parallel from v$instance "
        startup_time, version, parallel = super().query_one(sql,self.db_conn)
        uptime = datetime.datetime.now() - startup_time
        up_seconds = uptime.days * 86400 + uptime.seconds
        return up_seconds

    def get_oracle_pga(self):
        sql = """select value from v$pgastat where name = 'total PGA allocated'
                    """
        pga_size, = super().query_one(sql,self.db_conn)
        return round(pga_size/1024/1024,2)


    def get_oracle_sga(self):
        sql = """select sum(bytes) from v$sgainfo where name in (
                    'Fixed SGA Size',
                    'Redo Buffers',
                    'Buffer Cache Size',
                    'Shared Pool Size',
                    'Large Pool Size',
                    'Java Pool Size',
                    'Streams Pool Size',
                    'Shared IO Pool Size'
                )
            """
        sga_size, = super().query_one(sql,self.db_conn)
        sql = "select bytes from  v$sgainfo where name = 'Granule Size'"
        granu_size, = super().query_one(sql,self.db_conn)
        return round(int(sga_size+granu_size-1)/granu_size*granu_size/1024/1024,2)

    def get_oracle_mem(self):
        sga = self.get_oracle_sga()
        pga = self.get_oracle_pga()
        mem_phy = self.old_stat['PHYSICAL_MEMORY_BYTES']/1024/1024
        mem_pct = round(100*(pga+sga)/mem_phy,2)

        return {
            'sga_size': sga,
            'pga_size': pga,
            'memory_used_percent':mem_pct
        }

    def get_oracle_stat(self):
        if self.loop_cnt == 0:
            elapsed = self.get_uptime()
        else:
            elapsed = time.time() - self.last_time

        self.last_time = time.time()
        self.loop_cnt += 1
        orastat = {}
        orastat['os'] = self.oracle_osstat()
        orastat['stat'] = self.get_ora_stat(elapsed)
        orastat['wait'] = self.get_wait_events(elapsed)
        orastat['sess'] = self.get_oracle_session_count()
        orastat['load'] = self.get_oracle_load(elapsed)
        orastat['mem'] = self.get_oracle_mem()
        return orastat

    def get_ora_stat(self,elapsed):
        sql = """
                select name, value
                from v$sysstat
                where name in (%s)
                """
        stat_names = ",".join(("'" + s + "'" for s in self.ora_stats))
        sql_real = sql % (stat_names)
        res = super().query_all(sql_real,self.db_conn)
        stat_delta = {}
        for stat_name, stat_val in res:
            stat_delta[stat_name] = math.ceil((stat_val - self.old_stat[stat_name]) * 1.0 / elapsed)
            self.old_stat[stat_name] = stat_val

        return {
            'logons_cumulative': stat_delta['logons cumulative'],
            'qps': stat_delta['execute count'],
            'tps': stat_delta['user commits'] + stat_delta['transaction rollbacks'],
            'consistent_gets': stat_delta['consistent gets'],
            'logical_reads': stat_delta['session logical reads'],
            'physical_reads': stat_delta['physical reads'],
            'physical_writes': stat_delta['physical writes'],
            'block_changes': stat_delta['db block changes'],
            'redo_size': math.ceil(stat_delta['redo size'] / 1024),
            'total_parse_count': stat_delta['parse count (total)'],
            'hard_parse_count': stat_delta['parse count (hard)'],
            'bytes_received': math.ceil(stat_delta['bytes received via SQL*Net from client'] / 1024),
            'bytes_sent': math.ceil(stat_delta['bytes sent via SQL*Net to client'] / 1024),
            'exec_count': stat_delta['execute count'],
            'user_commits': stat_delta['user commits'],
            'user_rollbacks': stat_delta['user rollbacks'],
            'redo_writes': stat_delta['redo writes'],
            'io_throughput':round(stat_delta['physical read total bytes']/1024/1024 + stat_delta['physical write total bytes']/1024/1024,2)
        }

    def get_wait_events(self, elapsed):
        sql = """
              select /* dbagent */event, total_waits, round(time_waited_micro/1000,2) as time_waited
              from v$system_event
              where event in (%s)
          """
        event_names = ",".join("'" + s + "'" for s in self.wait_events)
        sql_real = sql % event_names
        res = super().query_all(sql_real,self.db_conn)

        stat_delta = defaultdict(int)
        for event, total_waits, time_waited in res:
            waits = total_waits - self.old_stat[event]
            if waits == 0:
                stat_delta[event + "/avg waitim"] = 0
                stat_delta[event] = 0
            else:
                stat_delta[event + "/avg waitim"] = math.ceil(
                    (time_waited - self.old_stat[event + "/time waited"]) * 1.0 / waits)
                stat_delta[event] = math.ceil(
                    (total_waits - self.old_stat[event]))

            self.old_stat[event] = total_waits
            self.old_stat[event + "/time waited"] = time_waited

        return {
            'log_file_sync_wait': stat_delta['log file sync/avg waitim'],
            'log_file_sync_count': stat_delta['log file sync'],
            'log_parallel_write_wait': stat_delta['log file parallel write/avg waitim'],
            'db_file_scattered_read_wait': stat_delta['db file scattered read/avg waitim'],
            'db_file_scattered_read_count': stat_delta['db file scattered read'],
            'db_file_sequential_read_wait': stat_delta['db file sequential read/avg waitim'],
            'db_file_sequential_read_count': stat_delta['db file sequential read'],
            'row_lock_wait_count': stat_delta['enq: TX - row lock contention']
        }

    def get_oracle_session_count(self):
        sql = """
            select count(*) as total_sess,
            sum(case when status='ACTIVE' and type = 'USER' then 1 else 0 end) as act_sess,
            sum(case when status='ACTIVE' and type = 'USER' and command in (2,6,7) then 1 else 0 end) as act_trans,
            sum(case when blocking_session is not null then 1 else 0 end) as blocked_sessions
        from v$session
        """
        #v$sqlcommand
        total_sess, act_sess, act_trans,blocked_sess = super().query_one(sql,self.db_conn)
        return {
            'total_sessions': total_sess,
            'active_sessions': act_sess,
            'active_trans_sessions': act_trans,
            'blocked_sessions':blocked_sess
        }

    def oracle_osstat(self):
        sql = """select stat_name, value from v$osstat
                where stat_name in ('PHYSICAL_MEMORY_BYTES', 'NUM_CPUS', 'IDLE_TIME', 'BUSY_TIME'
                )
            """
        res = super().query_all(sql,self.db_conn)
        cpu_idle = 0
        cpu_busy = 0

        for stat_name, value in res:
            if stat_name == 'IDLE_TIME':
                cpu_idle = value - self.old_stat[stat_name]
            elif stat_name == 'BUSY_TIME':
                cpu_busy = value - self.old_stat[stat_name]
            self.old_stat[stat_name] = value

        if cpu_idle + cpu_busy == 0:
            self.stat['host_cpu'] = 0
        else:
            self.stat['host_cpu'] = max(round(100.0 * cpu_busy / (cpu_idle + cpu_busy), 2), 0)

        return {
            'num_cpus': self.old_stat['NUM_CPUS'],
            'physical_memory': self.old_stat['PHYSICAL_MEMORY_BYTES']
        }


    def get_oracle_load(self,elapsed):
        stats = ",".join("'" + s + "'" for s in self.time_model)
        sql = """
                select stat_name, value
                from v$sys_time_model
                where stat_name in (%s)
            """ % stats
        res = super().query_all(sql,self.db_conn)
        stat_delta = {}
        num_cpu = self.old_stat.get('NUM_CPUS', 1)
        for stat_name, value in res:
            diff_val = max((value - self.old_stat[stat_name]) * 1.0 / elapsed, 0)
            if stat_name in ('DB time', 'DB CPU', 'background cpu time'):
                diff_val /= 10000.0 * num_cpu
            stat_delta[stat_name] = round(diff_val, 2)
            self.old_stat[stat_name] = value

        return {
            'dbtime': stat_delta['DB time'],
            'dbcpu': stat_delta['DB CPU'],
            'bgcpu': stat_delta['background cpu time']
        }

if __name__ =='__main__':
    oracle_params = {
        'host' : '192.168.48.10',
        'port':1521,
        'service_name':'pdb1',
        'user':'dbmon',
        'password':'oracle',
        'service_name_cdb':'orcl',
        'user_cdb':'c##dbmon',
        'password_cdb':'oracle'
    }
    db_conn = OracleBase(oracle_params).connection()
    oraclestat= OracleStat(oracle_params,db_conn)
    oraclestat.get_oracle_stat()
    time.sleep(1)
    oracle_data = oraclestat.get_oracle_stat()
    print(oracle_data)



















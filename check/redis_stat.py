#! /usr/bin/python
# encoding:utf-8

import redis
import re
import time

INFO_KEYS = (
"redis_version",
"uptime_in_days",
"redis_mode",
"connected_slaves",
"connected_clients",
"role",
"used_memory",
"used_memory_rss",
"mem_fragmentation_ratio",
"keyspace_hits",
"keyspace_misses")

STAT_KEYS = (
"keyspace_hits",
"keyspace_misses",
"total_commands_processed",
"total_net_input_bytes",
"total_net_output_bytes",
"expired_keys",
"evicted_keys"
)

COMMANDSTATS_KEYS = (
"cmdstat_brpop",
"cmdstat_publish",
"cmdstat_setnx",
"cmdstat_exec",
"cmdstat_multi"
)

CONFIG_KEYS = (
"maxmemory",
)


class RedisStat(object):
    def __init__(self,conn):
        self.conn=conn
        self.db_pattern = re.compile('^db(\d+)$')
        self.old_stat = {}
        self.old_commandstats = {}
        self.res = {'info':{},'stat':{},'commandstats':{},'config':{}}
        self.last_time = time.time()
        self.loop_cnt = 0
        for each in STAT_KEYS:
            self.old_stat[each] = 0
        for each in COMMANDSTATS_KEYS:
            self.old_commandstats[each] = 0
        for each in COMMANDSTATS_KEYS:
            self.res['commandstats'][each] = 0


    # 配置信息
    def get_redis_config(self):
        config =  self.conn.config_get()
        for conf_name in CONFIG_KEYS:
            conf_val = config.get(conf_name)
            self.res['config'][conf_name] = conf_val
        return config

    def get_redis_stat(self):
        total_keys = 0
        expire_keys = 0
        stat_now = self.conn.info()
        commandstat_now = self.conn.info('commandstats')
        if self.loop_cnt == 0:
            elapsed = stat_now['uptime_in_seconds']
        else:
            elapsed = time.time() - self.last_time
        for k,v in stat_now.items():
            if k in INFO_KEYS:
                self.res['info'][k] = v
            if k in STAT_KEYS:
                self.res['stat'][k] = round((v - self.old_stat[k])/elapsed,2)
            # 统计各库keys数量
            if self.db_pattern.match(k):
                total_keys += v['keys']
                expire_keys += v['expires']
            self.res['info']['total_keys'] = total_keys
            self.res['info']['expire_keys'] = expire_keys

        for k,v in commandstat_now.items():
            if k in COMMANDSTATS_KEYS:
                self.res['commandstats'][k] = round((v['calls'] - self.old_commandstats[k])/elapsed,2)
                self.old_commandstats[k] = v['calls']

        self.old_stat = stat_now
        self.last_time = time.time()
        self.loop_cnt += 1

if __name__ == "__main__":
    redis_conn = redis.StrictRedis(host='192.168.48.60', port=6379)
    the_redis = RedisStat(redis_conn)
    the_redis.get_redis_stat()
    time.sleep(1)
    the_redis.get_redis_stat()
    the_redis.get_redis_config()
    redis_data = the_redis.res





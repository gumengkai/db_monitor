# encoding:utf-8
from datetime import datetime,timedelta
from utils.tools import mysql_exec,mysql_query,now
from utils.redis_base import RedisBase
from utils.linux_base import LinuxBase
import re
import os

RedisKeyWordList=['ERROR','WARNING']

TZ_ADJUST = timedelta(hours=8)

def save_redis_log(tags,host,log_meta):
    check_time = now()
    for key in RedisKeyWordList:
        if log_meta:
            save = False
            if key in log_meta['log_content']:
                save = True
            if save:
                if 'log_time' in log_meta:
                    log_time = log_meta['log_time']
                else:
                    log_time = ''
                sql = "insert into alert_log(tags,host,type,log_time,log_level,log_content,check_time) values(%s,%s,%s,%s,%s,%s,%s)"
                values = (tags, host,'3',log_time, log_meta['log_level'], log_meta['log_content'],check_time)
                mysql_exec(sql, values)
                log_meta = []

def get_log_level_redis(log_content):
    if "ERROR" in log_content:
        return "error"
    elif "WARNING" in log_content:
        return "warn"
    else:
        return "info"

def parse_redis_logs(tags,host,log_stream):

    log_meta = {}
    reg_date = re.compile('(\d{2} [a-zA-Z]{3} \d{2}:\d{2}:\d{2})')

    log_buffer = []

    now_year = datetime.now().year

    for log_line, log_pos in log_stream:
        log_line = log_line.decode(encoding='utf-8')
        if log_line == '\n' or log_line == '':
            if len(log_buffer) > 0:
                log_content = "".join(log_buffer).strip()
                log_meta['log_content'] = log_content
                log_meta['log_level'] = get_log_level_redis(log_content)
                save_redis_log(tags,host,log_meta)
                log_buffer = []
            continue

        m = reg_date.search(log_line)
        if m:
            if len(log_buffer) > 0:
                log_content = "".join(log_buffer).strip()
                log_meta['log_content'] = log_content
                log_meta['log_level'] = get_log_level_redis(log_content)
                save_redis_log(tags,host,log_meta)
                log_buffer = []

            log_t, = m.groups()
            log_t = str(now_year) + ' ' + log_t

            if log_t is not None:
                log_time = datetime.strptime(log_t, '%Y %d %b %H:%M:%S')

            log_meta['log_time'] = str(log_time - TZ_ADJUST)
            log_meta['log_content'] = log_line.strip()
            log_meta['log_level'] = get_log_level_redis(log_line)
            save_redis_log(tags, host, log_meta)
            continue

        log_buffer.append(log_line)
        if len(log_buffer) > 100:
            log_content = "".join(log_buffer).strip()
            log_meta['log_content'] = log_content
            log_meta['log_level'] = get_log_level_redis(log_content)
            save_redis_log(tags, host, log_meta)
            log_buffer = []

    if len(log_buffer) > 0:
        log_content = "".join(log_buffer).strip()
        log_meta['log_content'] = log_content
        log_meta['log_level'] = get_log_level_redis(log_content)
        save_redis_log(tags, host, log_meta)
        log_buffer = []

    return log_pos

def get_redis_log(tags,redis_params,linux_params):
    host = redis_params['host']
    # logfile loglocation
    sql = "select log,log_seek from redis_list where tags='{}' ".format(tags)
    log,log_seek = mysql_query(sql)[0]
    if not log:
         redis_conn = RedisBase(redis_params).connection()
         log_dir = redis_conn.config_get('dir')['dir']
         log = redis_conn.config_get('logfile')['logfile']
         log = os.path.join(log_dir,log)
         log_seek = 0
         sql = "delete from alert_log where tags='{}' and type=3 ".format(tags)
         mysql_exec(sql)
    # get log content
    linux_oper = LinuxBase(linux_params)
    alert_content = linux_oper.readfile(log,seek=log_seek)
    # parse log
    log_seek = parse_redis_logs(tags,host,alert_content)
    # update alert log info to mysqlinfo
    sql = "update redis_list set log='{}',log_seek={} where tags='{}' " .format(log,log_seek,tags)
    mysql_exec(sql)

if __name__ =='__main__':
    redis_params = {
        'host': '192.168.48.60',
        'port': 6379,
        'version': '',
        'password': '',
        'user_os': 'root',
        'password_os': 'oracle',
        'sshport_os': 22
    }

    linux_params =   {
        'hostname': '192.168.48.60',
        'port': 22,
        'username':'root',
        'password':'oracle'
    }
    get_redis_log('redis-6379',redis_params,linux_params)

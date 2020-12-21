# encoding:utf-8
from datetime import datetime,timedelta
from utils.tools import mysql_exec,mysql_query,now
from utils.mysql_base import MysqlBase
from utils.mysql_do import Mysql_Do
from utils.linux_base import LinuxBase
import re

MysqlKeyWordList=['ERROR','Warning']

TZ_ADJUST = timedelta(hours=8)

def save_mysql_alert_log(tags,host,log_meta):
    check_time = now()
    for key in MysqlKeyWordList:
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
                values = (tags, host,'2',log_time, log_meta['log_level'], log_meta['log_content'],check_time)
                mysql_exec(sql, values)
                log_meta = []

def get_log_level_mysql(log_content):
    if "[ERROR]" in log_content:
        return "error"
    elif "[Warning]" in log_content:
        return "warn"
    else:
        return "info"

def parse_mysql_alert_logs(tags,host,log_stream):
    
    log_pos = 0
    log_meta = {}

    reg_date = re.compile('(\d{6} \d{2}:\d{2}:\d{2})|(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})|(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})')

    log_buffer = []

    for log_line, log_pos in log_stream:
        log_line = log_line.decode(encoding='utf-8')
        if log_line == '\n' or log_line == '':
            if len(log_buffer) > 0:
                log_content = "".join(log_buffer).strip()
                log_meta['log_content'] = log_content
                log_meta['log_level'] = get_log_level_mysql(log_content)
                save_mysql_alert_log(tags,host,log_meta)
                log_buffer = []
            continue

        m = reg_date.match(log_line)
        if m:
            if len(log_buffer) > 0:
                log_content = "".join(log_buffer).strip()
                log_meta['log_content'] = log_content
                log_meta['log_level'] = get_log_level_mysql(log_content)
                save_mysql_alert_log(tags,host,log_meta)
                log_buffer = []

            log_t1, log_t2,log_t3 = m.groups()
            if log_t2 is not None:
                log_time = datetime.strptime(log_t2, '%Y-%m-%d %H:%M:%S')
            elif log_t3 is not None:
                log_time = datetime.strptime(log_t3, '%Y-%m-%dT%H:%M:%S')
            else:
                log_time = datetime.strptime(log_t1, '%y%m%d %H:%M:%S')

            log_meta['log_time'] = str(log_time - TZ_ADJUST)
            log_meta['log_content'] = log_line.strip()
            log_meta['log_level'] = get_log_level_mysql(log_line)
            save_mysql_alert_log(tags, host, log_meta)
            continue

        log_buffer.append(log_line)
        if len(log_buffer) > 100:
            log_content = "".join(log_buffer).strip()
            log_meta['log_content'] = log_content
            log_meta['log_level'] = get_log_level_mysql(log_content)
            save_mysql_alert_log(tags, host, log_meta)
            log_buffer = []

    if len(log_buffer) > 0:
        log_content = "".join(log_buffer).strip()
        log_meta['log_content'] = log_content
        log_meta['log_level'] = get_log_level_mysql(log_content)
        save_mysql_alert_log(tags, host, log_meta)
        log_buffer = []

    return log_pos

def get_mysql_alert(tags,mysql_params,linux_params):
    host = mysql_params['host']
    # logfile loglocation
    sql = "select alert_log,alert_log_seek from mysql_list where tags='{}' ".format(tags)
    alert_log,alert_log_seek = mysql_query(sql)[0]
    if not alert_log:
        alert_log = Mysql_Do(mysql_params).get_para('log_error')
        alert_log_seek = 0
        sql = "delete from alert_log where tags='{}' and type=2 ".format(tags)
        mysql_exec(sql)
    if  alert_log:
        # get alert log content
        linux_oper = LinuxBase(linux_params)
        alert_content = linux_oper.readfile(alert_log, seek=alert_log_seek)
        # parse log
        alert_log_seek = parse_mysql_alert_logs(tags, host, alert_content)
        # update alert log info to mysqlinfo
        sql = "update mysql_list set alert_log='{}',alert_log_seek={} where tags='{}' ".format(alert_log,
                                                                                               alert_log_seek, tags)
        mysql_exec(sql)


if __name__ =='__main__':
    mysql_params = {
        'host': '192.168.48.51',
        'port': 3306,
        'user': 'root',
        'password': 'mysqld'
    }
    linux_params =   {
        'hostname': '192.168.48.51',
        'port': 22,
        'username':'root',
        'password':'mysqld'
    }
    get_mysql_alert('mysql-master',mysql_params,linux_params)

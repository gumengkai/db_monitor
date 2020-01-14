# encoding: utf-8
from datetime import datetime
from utils.oracle_base import query_one
from utils.linux_base import LinuxBase
from utils.tools import mysql_exec,mysql_query,now
from utils.oracle_base import get_connection

parse_result = []

OracleKeyWordList=['ORA-','WARNING:','Starting ORACLE instance','Shutting down instance']

def get_log_level_oracle(log_content):
    if 'ORA-' in log_content or 'Error' in log_content:
        return "error"
    elif 'WARNING:' in log_content:
        return "warn"
    elif 'Starting ORACLE instance' in log_content:
        return 'info'
    elif 'Shutting down instance' in log_content:
        return 'info'
    else:
        return "info"

def save_oracle_alert_log(tags,host,log_meta):
    for key in OracleKeyWordList:
        if log_meta:
            save = False
            save_type = '1'
            check_time = now()
            if key in log_meta['log_content']:
                save = True
            if save:
                if 'log_time' in log_meta:
                    log_time = log_meta['log_time']
                else:
                    log_time = ''

                sql = "insert into alert_log(tags,host,type,log_time,log_level,log_content,check_time)" \
                      "values(%s,%s,%s,%s,%s,%s,%s)"
                values = (tags,host,save_type,log_time,log_meta['log_level'],log_meta['log_content'],check_time)
                mysql_exec(sql,values)
                log_meta = []


def parse_oracle_alert_logs(tags,host,log_stream,version):
    """Wed Mar 02 14:00:30 2016"""
    # datetime.strptime(dt, '%a %b %d %H:%M:%S %Y')
    log_buffer = []
    log_meta = {}

    for log_line, log_pos in log_stream:
        try:
            log_line = log_line.decode(encoding='utf-8')
            log_line_strip = log_line.strip()
            if version == 'Oracle12c':
                log_time = datetime.strptime(log_line_strip, '%Y-%m-%dT%H:%M:%S.%f+08:00')
            else:
                log_time = datetime.strptime(log_line_strip, '%a %b %d %H:%M:%S %Y')

            match_time = True

        except ValueError:
            match_time = False

        if match_time:
            if len(log_buffer) > 0:
                log_content = "\r\n".join(log_buffer).strip()
                log_meta['log_content'] = log_content
                log_meta['log_level'] = get_log_level_oracle(log_content)
                save_oracle_alert_log(tags,host,log_meta)
                log_buffer = []


            log_meta['log_time'] = str(log_time)
        else:
            if log_line != '':
                log_buffer.append(log_line)

        if len(log_buffer) > 100:
            log_buffer = [str(each) if type(each)!=type('str') else each for each in log_buffer]
            print(log_buffer)
            for each in log_buffer:
                if type(each) != type('str'):
                    print(each)
            log_content = "\r\n".join(log_buffer).strip()
            log_meta['log_content'] = log_content
            log_meta['log_level'] = get_log_level_oracle(log_content)
            save_oracle_alert_log(tags,host,log_meta)
            log_buffer = []

    if len(log_buffer) > 0:
        log_content = "\r\n".join(log_buffer).strip()
        log_meta['log_content'] = log_content
        log_meta['log_level'] = get_log_level_oracle(log_content)
        save_oracle_alert_log(tags,host,log_meta)

    return log_pos


def get_oracle_alert(tags,db_conn,oracle_params,linux_params):
    db_version = oracle_params['db_version']
    host = oracle_params['host']
    # 取alert日志
    sql = "select alert_log,alert_log_seek from oracle_list where tags='{}' ".format(tags)
    alert_log,alert_log_seek = mysql_query(sql)[0]
    if not alert_log:
        sql = "select value from v$diag_info where name = 'Diag Trace'"
        alert_dir = query_one(db_conn, sql)
        # 取实例名
        sql = "select instance_name from v$instance"
        instance_name = query_one(db_conn, sql)
        alert_log = '{}/alert_{}.log'.format(alert_dir[0], instance_name[0])
        alert_log_seek = 0
        sql = "delete from alert_log where tags='{}' and type=1 ".format(tags)
        mysql_exec(sql)
    # ssh获取日志内容
    linux_oper = LinuxBase(linux_params)
    # 日志解析
    alert_content = linux_oper.readfile(alert_log,seek=alert_log_seek)
    alert_log_seek = parse_oracle_alert_logs(tags,host,alert_content,db_version)
    # 更新配置表中日志路径,日志偏移量
    sql = "update oracle_list set alert_log='{}',alert_log_seek={} where tags='{}' " .format(alert_log,alert_log_seek,tags)
    mysql_exec(sql)


if __name__ =='__main__':
    oracle_params = {
        'host' : '192.168.48.60',
        'port':1521,
        'service_name':'pdb1',
        'user':'dbmon',
        'password':'oracle',
        'service_name_cdb':'orcl19c',
        'user_cdb':'c##dbmon',
        'password_cdb':'oracle',
        'db_version' : 'Oracle12c'
    }
    linux_params =   {
        'hostname': '192.168.48.60',
        'port': 22,
        'username':'root',
        'password':'oracle'
    }
    db_conn = get_connection(oracle_params)

    get_oracle_alert('19cpdb1',db_conn,oracle_params,linux_params)


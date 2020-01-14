# encoding:utf-8

import re
from utils.tools import mysql_exec,mysql_query,now
from utils.mysql_do import Mysql_Do
from utils.linux_base import LinuxBase


def save_data(host,tags,SQL_META):
    check_time = now()
    if SQL_META:
        start_time = SQL_META['start_time']
        host_client = SQL_META['host']
        db_name = ''
        if 'db_name' in SQL_META:
            db_name = SQL_META['db_name']
        sql_text = SQL_META['sql_text']
        query_time = float(SQL_META['query_time'])
        lock_time = float(SQL_META['lock_time'])
        rows_examined = int(SQL_META['rows_examined'])
        rows_sent = int(SQL_META['rows_sent'])
        thread_id = SQL_META['thread_id']

        if not sql_text.startswith('commit'):
            sql = "insert into mysql_slowquery(host,tags,start_time,client_host,db_name,sql_text,query_time,lock_time," \
                  "rows_examined,rows_sent,thread_id,check_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            values = (
                host, tags, start_time, host_client, db_name, sql_text, query_time, lock_time,
                rows_examined,rows_sent, thread_id,check_time)

            mysql_exec(sql, values)

def parse_mysql_slowquery_logs(tags,host,log_stream):
    ## User@Host: root[root] @ localhost [127.0.0.1]  Id: 626474
    # Query_time: 0.230439  Lock_time: 0.000000 Rows_sent: 0  Rows_examined: 0
    #use dtops_test;

    SQL_META = {}

    reg_ts = re.compile('^SET timestamp=\d+;$')


    reg_time = re.compile('^# Time: ((\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.*?$)|((\d\d\d\d\d\d (?:\d| )\d:\d\d:\d\d)$))')
    # reg_host = re.compile('^# User@Host: (.+) @ (.*) \[(.*)\](?:  Id: (\d+))?$')
    reg_host = re.compile('^# User@Host:\s+(.*\])(?:\s+Id:\s+(\d+))?$')
    reg_querytime = re.compile('^# Query_time:\s+(\d+\.\d+)\s+Lock_time:\s+(\d+\.\d+)\s+Rows_sent:\s+(\d+)\s+Rows_examined:\s+(\d+)')
    reg_db = re.compile('^use ([^;]*);$')
    reg_schema = re.compile('^# Schema: (\w+)')
    reg_ignore = re.compile('^# Bytes_sent:')


    #state 0: before match
    #state 1: get time
    #state 2: get host
    #state 3: get query time
    #state 4: match sql
    sql_lines = []
    state = 0
    for log_l, f_pos in log_stream:
        log_l = log_l.decode(encoding='utf-8',errors="ignore")
        if state == 0:
            m = reg_time.match(log_l)
            if m:
                state = 1
                query_start_time = m.groups()[0]
                SQL_META['start_time'] = query_start_time
        elif state == 1:
            m = reg_host.match(log_l)
            if m:
                state = 2
                host, thread_id = m.groups()
                SQL_META['host'] = host
                SQL_META['thread_id'] = thread_id
        elif state == 2:
            m = reg_schema.match(log_l)
            if m:
                SQL_META['db_name'] = m.groups()[0]

            m = reg_querytime.match(log_l)
            if m:
                state = 3
                query_time, lock_time, rows_sent, rows_examined = m.groups()
                SQL_META['query_time'] = query_time
                SQL_META['lock_time'] = lock_time
                SQL_META['rows_sent'] = rows_sent
                SQL_META['rows_examined'] = rows_examined
        elif state == 3:
            m = reg_time.match(log_l)
            if m:
                query_start_time = m.groups()[0]
                state = 1
                if len(sql_lines) > 0:
                    sql_text = "".join(sql_lines).strip()
                    SQL_META['sql_text'] = sql_text
                    save_data(host,tags,SQL_META)

                sql_lines = []
                SQL_META['start_time'] = query_start_time
            elif log_l == '':
                sql_text = "".join(sql_lines).strip()
                SQL_META['sql_text'] = sql_text
                save_data(host, tags, SQL_META)

            else:
                # same query time
                m = reg_host.match(log_l)
                if m:
                    state = 2
                    host, thread_id = m.groups()

                    sql_text = "".join(sql_lines)
                    SQL_META['sql_text'] = sql_text.strip()
                    save_data(host,tags,SQL_META)

                    SQL_META['host'] = host
                    SQL_META['thread_id'] = thread_id
                    sql_lines = []
                else:
                    # /usr/sbin/mysqld, Version: 5.6.27-0ubuntu0.14.04.1 ((Ubuntu)). started with:
                    # Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock
                    # Time                 Id Command    Argument


                    if reg_ts.match(log_l) or log_l == '':
                        continue
                    else:
                        m = reg_db.match(log_l)
                        if m:
                            SQL_META['db_name'] = m.groups()[0]
                        else:
                            m = reg_ignore.match(log_l)
                            if m:
                                continue
                            sql_lines.append(log_l)

        #end of file
        if log_l == '':
            return f_pos


def get_mysql_slowquery(tags,mysql_params,linux_params):
    host = mysql_params['host']
    # slow query log location
    sql = "select slowquery_log,slowquery_log_seek from mysql_list where tags='{}' ".format(tags)
    slowquery_log,slowquery_log_seek = mysql_query(sql)[0]
    if not slowquery_log:
        slowquery_log = Mysql_Do(mysql_params).get_para('slow_query_log_file')
        slowquery_log_seek = 0
    # get slowquery log content
    linux_oper = LinuxBase(linux_params)
    slowquery_content = linux_oper.readfile(slowquery_log,seek=slowquery_log_seek)
    # parse log
    slowquery_log_seek = parse_mysql_slowquery_logs(tags,host,slowquery_content)
    # update alert log info to mysqlinfo
    sql = "update mysql_list set slowquery_log='{}',slowquery_log_seek={} where tags='{}' " .format(slowquery_log,slowquery_log_seek,tags)
    mysql_exec(sql)

if __name__ =='__main__':
    mysql_params = {
        'host': '192.168.48.50',
        'port': 3306,
        'user': 'root',
        'password': 'mysqld'
    }
    linux_params =   {
        'hostname': '192.168.48.50',
        'port': 22,
        'username':'root',
        'password':'mysqld'
    }
    get_mysql_slowquery('mysql50',mysql_params,linux_params)

# encoding:utf-8
import os
import pytz
from pytz import timezone
from datetime import datetime,timedelta
os.environ['DJANGO_SETTINGS_MODULE'] = 'db_monitor.settings'
from django.conf import settings
from utils.mysql_base import MysqlBase
from check.linux_stat import LinuxStat

HOST= settings.DATABASES['default']['HOST']
PORT= settings.DATABASES['default']['PORT']
NAME= settings.DATABASES['default']['NAME']
USER= settings.DATABASES['default']['USER']
PASSWORD= settings.DATABASES['default']['PASSWORD']

mysql_params = {
    'host':HOST,
    'port':PORT,
    'user':USER,
    'password':PASSWORD,
    'db':NAME
}

utc_tz = pytz.timezone('UTC')


def mysql_query(sql):
    res = MysqlBase(mysql_params).query(sql)
    return res

def mysql_django_query(sql):
    res = MysqlBase(mysql_params).django_query(sql)
    return res

def mysql_exec(sql,value=''):
    if not value:
        MysqlBase(mysql_params).exec(sql, '')
    else:
        MysqlBase(mysql_params).exec(sql, value)

def init_table(tab,tags):
    sql = "insert into {}_his select * from {} where tags={}".format(tab,tab,tags)
    mysql_exec(sql)
    sql = "delete from {} where tags={}".format(tab,tags)
    mysql_exec(sql)

def now():
    return datetime.now(tz=utc_tz).strftime('%Y-%m-%d %H:%M:%S')

def now_local():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def today():
    return datetime.now(tz=utc_tz)

def last_day():
    return (datetime.now(tz=utc_tz) - timedelta(days=1))

def clear_table(tags,table_name):
    sql = "delete from {} where tags='{}' ".format(table_name,tags)
    mysql_exec(sql)

def archive_table(tags,table_name):
    sql = "insert into {}_his select * from {} where tags='{}' ".format(table_name,table_name,tags)
    mysql_exec(sql)

def get_utctime(loctime):
    return datetime.strptime(loctime,'%Y-%m-%d %H:%M:%S').astimezone(pytz.utc)

def get_redis_params(tags):
    sql = "select t1.tags,t1.host,t1.port,t1.redis_version,t1.password,t2.user,t2.password,t2.sshport" \
          " from redis_list t1 inner join linux_list t2 on t1.linux_tags=t2.tags where t1.tags= '{}'".format(tags)
    res = mysql_query(sql)[0]
    return {
        'host': res[1],
        'port': res[2],
        'version': res[3],
        'password': res[4],
        'user_os': res[5],
        'password_os': res[6],
        'sshport_os': res[7]
    }

def get_oracle_params(tags):
    sql = "select t1.tags,t1.host,t1.port,t1.service_name,t1.db_user,t1.db_password,t1.db_user_cdb,t1.db_password_cdb,t1.service_name_cdb," \
          "t2.user,t2.password,t2.sshport,t1.db_version from oracle_list t1 inner join linux_list t2  on t1.linux_tags=t2.tags where t1.tags='{}' ".format(tags)
    res = mysql_query(sql)[0]
    return  {
        'host': res[1],
        'port': res[2],
        'service_name': res[3],
        'user': res[4],
        'password': res[5],
        'user_cdb': res[6],
        'password_cdb': res[7],
        'service_name_cdb': res[8],
        'user_os': res[9],
        'password_os': res[10],
        'sshport_os': res[11],
        'db_version': res[12]
    }

def get_memtotal(host,password):
    linux_params = {
        'hostname': host,
        'port': 22,
        'username': 'root',
        'password': password
    }
    linuxstat = LinuxStat(linux_params,'')
    memtotal = linuxstat.get_memtotal()['memtotal']
    return memtotal

if __name__ == '__main__':
    loctime = '2019-12-10 08:30:39'
    print(type(get_utctime(loctime)))
    print(now())

# encoding:utf-8

from check.check_oracle import check_oracle
from check.check_linux import check_linux
from check.check_mysql import check_mysql
from check.check_redis import check_redis
from check.alarm import check_alarm
from utils.tools import clear_table,archive_table,mysql_query
from multiprocessing import Process

def checkall():
    # all minitoring servers
    linux_list = mysql_query('select tags,host,sshport,user,password from linux_list')
    oracle_list = mysql_query(
        'select t1.tags,t1.host,t1.port,t1.service_name,t1.db_user,t1.db_password,t1.db_user_cdb,t1.db_password_cdb,t1.service_name_cdb,'
        't2.user,t2.password,t2.sshport,t1.db_version from oracle_list t1 left join linux_list t2  on t1.linux_tags=t2.tags ')

    mysql_list = mysql_query(
        'select t1.tags,t1.host,t1.port,t1.db_user,t1.db_password,t2.user,t2.password,t2.sshport,t1.db_version'
        ' from mysql_list t1 left join linux_list t2 on t1.linux_tags=t2.tags')

    redis_list = mysql_query(
        'select t1.tags,t1.host,t1.port,t1.redis_version,t1.password,t2.user,t2.password,t2.sshport'
        ' from redis_list t1 left join linux_list t2 on t1.linux_tags=t2.tags')

    # check_linux
    check_pool = []

    if linux_list:
        for each in linux_list:
            tags = each[0]
            linux_params = {
                'hostname': each[1],
                'port': each[2],
                'username':  each[3],
                'password': each[4]
            }
            linux_check = Process(target=check_linux,args=(tags,linux_params))
            linux_check.start()
            check_pool.append(linux_check)

    if oracle_list:
        for each in oracle_list:
            tags = each[0]
            oracle_params = {
                'host': each[1],
                'port': each[2],
                'service_name': each[3],
                'user': each[4],
                'password': each[5],
                'user_cdb': each[6],
                'password_cdb': each[7],
                'service_name_cdb': each[8],
                'user_os': each[9],
                'password_os': each[10],
                'sshport_os': each[11],
                'db_version': each[12]
            }
            oracle_check = Process(target=check_oracle, args=(tags, oracle_params))
            oracle_check.start()
            check_pool.append(oracle_check)

    if mysql_list:
        for each in mysql_list:
            tags = each[0]
            mysql_params = {
                'host': each[1],
                'port': each[2],
                'user': each[3],
                'password': each[4],
                'user_os': each[5],
                'password_os': each[6],
                'sshport_os':each[7]
            }
            mysql_check = Process(target=check_mysql, args=(tags, mysql_params))
            mysql_check.start()
            check_pool.append(mysql_check)

    if redis_list:
        for each in redis_list:
            tags = each[0]
            redis_params = {
                'host': each[1],
                'port': each[2],
                'version': each[3],
                'password': each[4],
                'user_os': each[5],
                'password_os': each[6],
                'sshport_os':each[7]            }
            redis_check = Process(target=check_redis, args=(tags, redis_params))
            redis_check.start()
            check_pool.append(redis_check)

    for each in check_pool:
        each.join()

    # 告警
    check_alarm()




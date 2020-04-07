# encoding:utf-8

from utils.tools import mysql_exec,mysql_query,now,archive_table,clear_table
import check.checklog as checklog
from utils.send_email import my_send_email

def check_alarm():
    alarm_time = now()
    checklog.logger.info('初始化告警信息表')
    mysql_exec('insert into alarm_info_his select * from alarm_info')
    mysql_exec('delete from alarm_info')
    check_list = mysql_query(
        "select name,judge_value,judge_sql,judge_table,conf_table,conf_column from alarm_conf where judge_sql is not null and judge_table is not null")
    for each_check in check_list:
        alarm_name, judge_value,judge_sql,judge_table,conf_table,conf_column = each_check
        checklog.logger.info("开始告警检查：{}" .format(alarm_name))
        select_sql = "select count(*) from {}".format(judge_table)
        select_res = mysql_query(select_sql)
        if select_res[0][0] == 0:
            checklog.logger.info("%s未采集到数据" % alarm_name)
        else:
            is_judge_sql = ' tags in (select tags from {} where {} =1)'.format(conf_table,conf_column)
            judge_sql = judge_sql % (judge_value,is_judge_sql) if judge_value else judge_sql % is_judge_sql
            check_res = mysql_query(judge_sql)
            if check_res == 0:
                checklog.logger.info("{}:告警检查正常" % alarm_name)
            else:
                for each in check_res:
                    tags,url,alarm_content = each
                    alarm_title = tags + ':' + alarm_name
                    insert_sql = "insert into alarm_info (tags,url,alarm_type,alarm_header,alarm_content,alarm_time) values('{}','{}','{}','{}','{}','{}') ".format(
                        tags, url, alarm_name, alarm_title, alarm_content,alarm_time)
                    checklog.logger.warning(alarm_content)
                    mysql_exec(insert_sql)
                    # is_send_email(alarm_name, tags, alarm_url, alarm_title, alarm_content)
                    my_send_email(alarm_title,alarm_content)

if __name__ == '__main__':
    check_alarm()


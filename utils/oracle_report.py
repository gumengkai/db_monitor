#! /usr/bin/python
# ecoding:utf-8

from utils.tools import *
from utils.oracle_base import OracleBase
import time,os,cx_Oracle,codecs
from datetime import datetime

class OracleReport(OracleBase):
    def __init__(self,db_conn,tags,params):
        super().__init__(params)
        self.db_conn = db_conn
        self.tags = tags
        self.params = params

    def get_awr(self,dbid,instance_name,begin_snap,end_snap):

        sql = """
                    select output from table(
                        dbms_workload_repository.awr_report_html(
                            {},
                            {},
                            {},
                            {},
                        0))
                """.format(dbid,instance_name,begin_snap,end_snap)
        awr_content = super().query_all(sql,self.db_conn)
        return awr_content

    def get_addm(self,instance_name, dbid, instance_num, begin_snap, end_snap):

        desc = 'ADDM run: snapshots [ {}, {} ], instance {}, database id {}' .format(
            begin_snap, end_snap, instance_name, dbid)

        sql_create_task = """begin
                dbms_advisor.create_task('ADDM', :id, :name, :descr, null);
                dbms_advisor.set_task_parameter(:name, 'START_SNAPSHOT', :bid);
                dbms_advisor.set_task_parameter(:name, 'END_SNAPSHOT', :eid);
                dbms_advisor.set_task_parameter(:name, 'INSTANCE', :inst_num);
                dbms_advisor.set_task_parameter(:name, 'DB_ID', :dbid);
                dbms_advisor.execute_task(:name);
                end;
            """

        cur = self.db_conn.cursor()

        id = cur.var(cx_Oracle.NUMBER)
        name = cur.var(cx_Oracle.STRING)

        cur.execute(sql_create_task, {
            'id': id,
            'name': name,
            'descr': desc,
            'bid': begin_snap,
            'eid': end_snap,
            'inst_num': instance_num,
            'dbid': dbid})

        sql_get_report = "select dbms_advisor.get_task_report(:task_name, 'TEXT', 'TYPICAL') from sys.dual"
        cur.execute(sql_get_report, {'task_name': name.getvalue()})
        ret, = cur.fetchone()
        return [(ret.read(),)]


    def get_ash(self,dbid,instance_num,report_begin_time,report_end_time):

        sql = """select output from table (
                        DBMS_WORKLOAD_REPOSITORY.ASH_REPORT_HTML(
                        {},
                        {},
                        TO_DATE('{}','YYYY-MM-DD HH24:MI:SS'),
                        TO_DATE('{}','YYYY-MM-DD HH24:MI:SS')
                     ))
                """.format(dbid,instance_num,report_begin_time,report_end_time)

        res = super().query_all(sql,self.db_conn)
        return res

    def save_report(self,filename,data):
        with codecs.open(filename, 'w', 'utf-8') as f:
            for l in data:
                if l and l[0]:
                    content = l[0]
                    f.write(content + '\n')

    def get_report(self,report_type,begin_snap,end_snap):
        sql = "select instance_number,instance_name from v$instance"
        res = super().query_one(sql,self.db_conn)
        instance_num,instance_name = res

        sql = "select dbid from v$database"
        res = super().query_one(sql,self.db_conn)
        dbid = res[0]

        if report_type == 'ash':
            report_begin_time = datetime.strptime(begin_snap,"%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=8)
            report_end_time = datetime.strptime(end_snap,"%Y-%m-%dT%H:%M:%S.%fZ")  + timedelta(hours=8)
        else:
            sql = "select to_char(a.end_interval_time,'yyyy-mm-dd hh24:mi:ss') from dba_hist_snapshot a where a.snap_id=%s" % begin_snap
            res = super().query_one(sql,self.db_conn)
            report_begin_time = res[0]
            sql = "select to_char(a.end_interval_time,'yyyy-mm-dd hh24:mi:ss') from dba_hist_snapshot a where a.snap_id=%s" % end_snap
            res = self.query_one(sql,self.db_conn)
            report_end_time = res[0]

        if report_type == 'awr':
            data = self.get_awr(dbid, instance_num, begin_snap, end_snap)
        elif report_type == 'addm':
            data = self.get_addm(instance_name, dbid, instance_num, begin_snap, end_snap)
        else:
            data = self.get_ash(dbid, instance_num, report_begin_time, report_end_time)

        if report_type == 'addm':
            suffix = 'txt'
        else:
            suffix = 'html'
        if report_type == 'ash':
            cur_time = time.strftime('%H%M%S')
            report_name = '{}_{}_{}_{}.{}'.format(
                report_type, dbid, instance_num, cur_time, suffix)
        else:
            report_name = '{}_{}_{}_{}_{}.{}'.format(
                report_type, dbid, instance_num, begin_snap, end_snap, suffix)

        # report_file = os.getcwd() +  '/oracle/report/' +report_name
        report_file = os.getcwd() + '/templates/report/oracle/' + report_name
        self.save_report(report_file, data)
        insert_sql = " INSERT INTO oracle_report(tags,begin_time,end_time,report_type,file_path,status,create_time) " \
                     "values('{}','{}','{}','{}','{}','0','{}') ".format(
        self.tags, report_begin_time, report_end_time, report_type, 'report/oracle/'+report_name,now())
        mysql_exec(insert_sql, '')


if __name__ == '__main__':
    tags = 'pdb1'
    oracle_params = {
        'host': '192.168.48.60',
        'port': 1521,
        'service_name': 'pdb1',
        'user': 'dbmon',
        'password': 'oracle',
        'service_name_cdb': 'orcl19c',
        'user_cdb': 'c##dbmon',
        'password_cdb': 'oracle'
    }
    report_type = 'addm'
    begin_snap = '1958'
    end_snap = '1960'
    db_conn = OracleBase(oracle_params).connection()
    db_conn_cdb = OracleBase(oracle_params).connection_cdb()
    oracle_report = OracleReport(db_conn_cdb,tags,oracle_params)
    oracle_report.get_report(report_type,1958,1960)


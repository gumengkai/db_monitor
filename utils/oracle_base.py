# encoding:utf-8

import cx_Oracle

class OracleBase(object):
    def __init__(self, params):
        self.params = params
        self.host = self.params['host']
        self.port = self.params['port']
        self.service_name = self.params['service_name']
        self.user = self.params['user']
        self.password = self.params['password']
        self.service_name_cdb = self.params['service_name_cdb']
        self.user_cdb = self.params['user_cdb']
        self.password_cdb = self.params['password_cdb']

    def connection(self):
        oracle_url = '{}:{}/{}'.format(self.host, self.port, self.service_name)
        try:
            conn = cx_Oracle.connect(self.user, self.password, oracle_url)
            return conn
        except Exception as e:
            print('oracle connect error:{}'.format(e))

    def connection_cdb(self):
        oracle_url = cx_Oracle.makedsn(self.host, self.port, self.service_name_cdb)
        try:
            conn = cx_Oracle.connect(self.user_cdb, self.password_cdb, oracle_url)
            return conn
        except Exception as e:
            print('oracle connect error:{}'.format(e))

    def query_all(self,sql,db_conn=None):
        if not db_conn:
            db_conn = self.connection()
        try:
            cur = db_conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            return res
        except Exception as e:
            print('oracle query error:{}'.format(e))

    def query_one(self,sql,db_conn=None):
        if not db_conn:
            db_conn = self.connection()
        try:
            cur = db_conn.cursor()
            cur.execute(sql)
            res = cur.fetchone()
            return res
        except Exception as e:
            print('oracle query error:{}'.format(e))

    def django_query(self,sql,db_conn=None):
        if not db_conn:
            db_conn = self.connection()
        try:
            cursor = db_conn.cursor()
            count = cursor.execute(sql)
            if count == 0:
                result = 0
            else:
                desc = cursor.description
                return [
                    dict(zip([col[0] for col in desc], row))
                    for row in cursor.fetchall()
                ]
            cursor.close()
        except Exception as e:
            print('oracle query error:{}'.format(e))

    def call_proc(self,proc,db_conn=None):
        if not db_conn:
            db_conn = self.connection()
        try:
            cursor = db_conn.cursor()
            cursor.callproc(proc)
            cursor.close()
        except Exception as e:
            print('oracle query error:{}'.format(e))

def get_connection(params):
    host = params['host']
    port = params['port']
    service_name = params['service_name']
    user = params['user']
    password = params['password']
    oracle_url = '{}:{}/{}'.format(host,port,service_name)
    try:
        conn = cx_Oracle.connect(user, password, oracle_url)
        return conn
    except Exception as e:
        print('oracle connect error:{}'.format(e))

def get_connection_cdb(params):
    host = params['host']
    port = params['port']
    service_name = params['service_name_cdb']
    user = params['user_cdb']
    password = params['password_cdb']
    oracle_url = '{}:{}/{}'.format(host,port,service_name)
    try:
        conn = cx_Oracle.connect(user, password, oracle_url)
        return conn
    except Exception as e:
        print('oracle connect error:{}'.format(e))

def query_all(db_conn,sql):
    try:
        cur = db_conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        return res
    except Exception as e:
        print('oracle query error:{}'.format(e))

def query_one(db_conn,sql):
    try:
        cur = db_conn.cursor()
        cur.execute(sql)
        res = cur.fetchone()
        return res
    except Exception as e:
        print('oracle query error:{}'.format(e))

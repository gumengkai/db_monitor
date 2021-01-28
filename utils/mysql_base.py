# encoding:utf-8
import pymysql

class MysqlBase(object):
    def __init__(self,params):
        self.params = params
        self.host = self.params['host']
        self.user = self.params['user']
        self.port = self.params['port']
        self.password = self.params['password']
        self.db = self.params.get('db','mysql')
        self.conn_conf = {
            'connect_timeout': 5,
            'use_unicode': True,
            'charset': 'utf8'
        }

    def connection(self):
        self.params.update(self.conn_conf)
        try:
            conn = pymysql.connect(host=self.host,port=int(self.port),user=self.user,password=self.password,db=self.db)
            return conn
        except Exception as e:
            print('mysql connect error:{}'.format(e))

    def query(self,sql,conn=None):
        if not conn:
            conn = self.connection()
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

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
            print('mysql query error:{}'.format(e))

    def exec(self,sql,val):
        conn = self.connection()
        cur = conn.cursor()
        if val:
            cur.execute(sql, val)
        else:
            cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()


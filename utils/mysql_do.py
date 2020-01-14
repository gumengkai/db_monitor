# encoding:utf-8
from .mysql_base import  MysqlBase

class Mysql_Do(MysqlBase):
    def __init__(self,params):
        self.params = params
        self.db_host = self.params['host']
        self.db_user = self.params['user']
        self.db_password = self.params['password']
        self.db_port = self.params['port']
        super(Mysql_Do, self).__init__(self.params)
    # 取参数配置
    def get_para(self,paraname):
        sql = "show global variables like '{}' " .format(paraname)
        res = self.query(sql)
        return res[0][1]


# encoding： utf-8

from utils.linux_base import LinuxBase
from utils.tools import now_local
from utils.tools import mysql_exec,mysql_query,now,get_memtotal
import os
import configparser

class MysqlInstall():
    def __init__(self, node_info):
        self.node_info = node_info
        self.local_path = os.getcwd() + '/utils/mysql_install/'
        self.soft_path = {
            'MySQL5.7': 'mysql-5.7.33-linux-glibc2.12-x86_64.tar.gz'
        }

    def clear_log(self):
        sql = 'truncate table setup_log'
        mysql_exec(sql,)

    def log(self,log_content):
        log_level = 'info'
        log_type = 'MySQL安装'
        current_time = now_local()
        print('{}: {}'.format(current_time,log_content))
        sql = "insert into setup_log(log_type,log_time,log_level,log_content)" \
              "values(%s,%s,%s,%s)"
        values = (log_type,current_time,log_level,log_content)
        mysql_exec(sql, values)
    
    def linux_config(self,linux_conn,linux_params):
        cmd_list = [
            'systemctl stop firewalld',
            'systemctl disable firewalld',
            "sed -i 's/SELINUX=enabled/SELINUX=disabled/g' /etc/selinux/config ", #关闭防火墙，selinux
            'move /etc/my.cnf /etc/my.cnfbak', #移除旧的MySQL参数文件
            'yum search libaio',
            'yum install libaio', #安装libaio包
            'userdel -r mysql',
            'groupadd mysql',
            'useradd -g mysql -G mysql mysql',
            "echo 'mysql:mysqld'|chpasswd", #创建MySQL用户
            ]

        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]

    def create_mysql_dir(self,linux_conn,linux_params):
        mysql_path = self.node_info['mysql_path']
        data_path = self.node_info['data_path']
        mysql_run = '{}/run' .format(mysql_path)
        mysql_tmp = '{}/tmp'.format(mysql_path)
        mysql_undo = '{}/undo'.format(mysql_path)
        dirs = (mysql_path,data_path,mysql_run,mysql_tmp,mysql_undo)
        cmd_list = ['mkdir -p {}'.format(dir) for dir in dirs]

        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
    
    def generate_mysql_cnf(self):
        mycnf = 'my.cnf_new'
        # 读取模板配置文件
        cnf_template = '{}my.cnf.template.5.7'.format(self.local_path) if self.node_info['version'] == 'MySQL5.7' else '{}my.cnf.template.8.0'.format(self.local_path)
        parser = configparser.ConfigParser()
        conf_temp = parser.read(cnf_template)
        conf_dict = self.get_mysql_cnf()
        for section,section_val in conf_dict:
            for para_name,para_val in section_val:
                conf_temp.set(section,para_name,para_val)
                print(section,para_name,para_val)
        with open(mycnf,'w') as cnf_new:
            conf_temp.write(cnf_new)
    
    def get_mysql_cnf(self):
        mysql_path = self.node_info['mysql_path']
        data_path = self.node_info['data_path']
        socket = '{}/run/mysql.sock'.format(self.node_info['mysql_path'])
        slow_query_log_file = '{}/slow.log'.format(data_path)
        log_error = '{}/error.log'.format(data_path)
        log_bin = '{}/mybinlog'.format(data_path)
        innodb_undo_directory = '{}/undolog'.format(data_path)

        # innodb buffer pool大小设置为物理内存*0.7
        memory_size = float(self.node_info['memory'])
        innodb_buffer_pool_size = str(memory_size*0.7) + 'G'

        return {
            'client': {
                'socket': socket
            },
            'mysqld': {
                'basedir': mysql_path,
                'datadir': data_path,
                'socket': socket,
                'slow_query_log_file': slow_query_log_file,
                'log-error': log_error,
                'log-bin': log_bin,
                'innodb_undo_directory': innodb_undo_directory,
                'innodb_buffer_pool_size': innodb_buffer_pool_size
            }
        }


    def do_mysql_install(self ):
        linux_params = {
            'hostname': self.node_info['ip'],
            'port': 22,
            'username': 'root',
            'password': self.node_info['password']
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        self.linux_config(linux_conn,linux_params)
        self.create_mysql_dir(linux_conn,linux_params)
        self.generate_mysql_cnf()




if __name__ == '__main__':
    node_info = {
        'node_ip': '192.168.48.51',
        'hostname': 'cispdg',
        'dbname': 'cispcdb',
        'pdbname': 'cisp',
        'password': 'oracle',
    }

    oracleracinstall = OracleOneNodeInstall(node_info)
    # oracleracinstall.clear_rac()
    oracleracinstall.do_rac_install('linux')

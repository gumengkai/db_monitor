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
        self.mysql_soft_config = {
            'MySQL5.7': 'mysql-5.7.33-linux-glibc2.12-x86_64.tar.gz',
            'MySQL8.0': 'mysql-8.0.23-linux-glibc2.12-x86_64.tar.xz'
        }
        self.mysql_template_config = {
            'MySQL5.7': 'my.cnf.template.5.7',
            'MySQL8.0': 'my.cnf.template.8.0'
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
        self.log('开始进行linux基础配置..')
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
        self.log('{}：linux操作系统配置完成'.format(self.node_info['ip']))

    def create_mysql_dir(self,linux_conn,linux_params):
        self.log('开始创建MySQL目录..')
        mysql_path = self.node_info['mysql_path']
        data_path = self.node_info['data_path']
        mysql_run = '{}/run' .format(mysql_path)
        mysql_tmp = '{}/tmp'.format(mysql_path)
        mysql_undo = '{}/undo'.format(mysql_path)
        dirs = (mysql_path,data_path,mysql_run,mysql_tmp,mysql_undo)
        cmd_list = [
            'rm -rf  {}'.format(mysql_path),
            'rm -rf  {}'.format(data_path)
            ]

        cmd_list.extend(['mkdir -p {}'.format(dir) for dir in dirs])

        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('{}：创建目录完成'.format(self.node_info['ip']))

    
    def generate_mysql_cnf(self,linux_conn,linux_params):
        self.log('开始生成MySQL配置文件..')
        mysql_path = self.node_info['mysql_path']
        data_path = self.node_info['data_path']
        mysql_port = self.node_info['port']

        # innodb buffer pool大小设置为物理内存*0.7
        memory_size = float(self.node_info['memory'])
        innodb_buffer_pool_size = str(int(memory_size*0.7*1024)) + 'M'

        cnf_template = '{}my.cnf.template.5.7'.format(self.local_path) if self.node_info['version'] == 'MySQL5.7' else '{}my.cnf.template.8.0'.format(self.local_path)
        LinuxBase(linux_params).sftp_upload_file(cnf_template, '/tmp/my.cnf')
        cmd_list = [
            'mv /tmp/my.cnf {}/my.cnf'.format(mysql_path),
            "sed -i 's#MYSQL_PATH#{}#g' {}/my.cnf".format(mysql_path,mysql_path),
            "sed -i 's#DATA_PATH#{}#g' {}/my.cnf".format(data_path,mysql_path),
            "sed -i 's/INNODB_SIZE/{}/g' {}/my.cnf".format(innodb_buffer_pool_size,mysql_path),
            "sed -i 's/MYSQL_PORT/{}/g' {}/my.cnf".format(mysql_port,mysql_path)
        ]
        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('{}：MySQL配置文件生成完成'.format(self.node_info['ip']))
    
    def mysql_initialize(self,linux_conn,linux_params):
        mysql_path = self.node_info['mysql_path']
        data_path = self.node_info['data_path']

        mysql_package = self.mysql_soft_config[self.node_info['version']]
        # 上传
        self.log('开始上传MySQL安装包：{}..'.format(mysql_package))
        LinuxBase(linux_params).sftp_upload_file('{}{}'.format(self.local_path,mysql_package), '/tmp/{}'.format(mysql_package))
        self.log('{}：MySQL安装包上传完成'.format(self.node_info['ip']))

        # 解压
        self.log('开始解压MySQL安装包..')
        cmd = 'tar xvf /tmp/{} -C {}/'.format(mysql_package,mysql_path)
        LinuxBase(linux_params).exec_command_res(cmd,linux_conn)
        self.log('{}：MySQL安装包解压完成'.format(self.node_info['ip']))
        # 授权
        cmd_list = [
            'mv {}/mysql*/* {}'.format(mysql_path,mysql_path),
            'chown -R mysql:mysql {}'.format(mysql_path),
            'chmod -R 775 {}'.format(mysql_path),
            'chown -R mysql:mysql {}'.format(data_path),
            'chmod -R 775 {}'.format(data_path),
        ]
        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('开始初始化MySQL..')
        # 初始化
        cmd = '{}/bin/mysqld --defaults-file={}/my.cnf --initialize-insecure --user=mysql'.format(mysql_path,mysql_path)
        LinuxBase(linux_params).exec_command_res(cmd,linux_conn)
        self.log('{}：MySQL初始化完成'.format(self.node_info['ip']))
        self.log('请使用MySQL用户(默认密码mysqld)启动MySQL数据库：{}/bin/mysqld_safe --defaults-file={}/my.cnf --user=mysql &'.format(mysql_path,mysql_path))
        # 启动
        # cmd = '{}/bin/mysqld_safe --defaults-file={}/my.cnf --user=mysql &'.format(mysql_path,mysql_path)
        # LinuxBase(linux_params).exec_command_res(cmd,linux_conn)

        
    def do_mysql_install(self ):
        linux_params = {
            'hostname': self.node_info['ip'],
            'port': 22,
            'username': 'root',
            'password': self.node_info['password']
        }
        self.clear_log()
        linux_conn, _ = LinuxBase(linux_params).connection()
        self.linux_config(linux_conn,linux_params)
        self.create_mysql_dir(linux_conn,linux_params)
        self.generate_mysql_cnf(linux_conn,linux_params)
        self.mysql_initialize(linux_conn,linux_params)


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

# encoding： utf-8

from utils.linux_base import LinuxBase
from utils.tools import now_local
from utils.tools import mysql_exec,mysql_query,now,get_memtotal
import os

class OracleOneNodeInstall():
    def __init__(self, node_info):
        self.node_info = node_info
        self.linux_group_list = [
            [501, 'dba'],
            [502, 'oinstall'],
            [503, 'oper']
        ]
        self.linux_user_list = {
            'oracle': 501
        }
        self.linux_packages = "openssh bc binutils compat-libcap1 compat-libstdc++ elfutils-libelf elfutils-libelf-devel fontconfig-devel glibc " \
                              "glibc-devel ksh libaio libaio-devel libX11 libXau libXi libXtst libXrender libXrender-devel libgcc librdmacm-devel " \
                              "libstdc++ libstdc++-devel libxcb make smartmontools sysstat gcc-c++ nfs-utils net-tools unzip expect"

        self.local_path = os.getcwd() + '/utils/oracle_rac_install/'


    def clear_log(self):
        sql = 'truncate table setup_log'
        mysql_exec(sql,)

    def log(self,log_content):
        log_level = 'info'
        log_type = 'Oracle One Node安装'
        current_time = now_local()
        print('{}: {}'.format(current_time,log_content))
        sql = "insert into setup_log(log_type,log_time,log_level,log_content)" \
              "values(%s,%s,%s,%s)"
        values = (log_type,current_time,log_level,log_content)
        mysql_exec(sql, values)

    def clear_rac(self):
        self.log('开始清理Oracle RAC')
        # 删除目录
        cmd_list = [
            'rm -rf /u01',
            'rm -f /usr/local/bin/dbhome',
            'rm -f /usr/local/bin/oraenv',
            'rm -f /usr/local/bin/coraenv',
            'rm -f /etc/oratab',
            'rm -f /etc/oraInst.loc',
            'rm -rf /etc/oracle',
            'rm -rf /etc/ora*',
            'rm -rf /etc/init/oracle*',
            'rm -rf /etc/init.ohasd',
            'rm -rf /etc/ohasd',
            'rm -rf /etc/init.tfa',
            'rm -rf /var/tmp/.oracle',
            'rm -rf /tmp/CVU*',
            'rm -rf /tmp/OraInstall*',
            'rm -rf /var/tmp/.oracle',
            'rm -rf /opt/oracle'
        ]
        # 删除用户组
        cmd_list.extend(
            ['groupdel {}'.format(group[1]) for group in self.linux_group_list]
        )
        # 删除用户
        cmd_list.extend(
            ['userdel -rf oracle'],
        )
        # 清理完成后重启服务器
        cmd_list.extend(
            ['reboot']
        )
        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'root',
            'password': self.node_info['node_password']
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        self.log('{}：开始清理Oracle RAC！'.format(self.node_info['node_ip']))
        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('Oracle RAC清理完成！')


    def upload_software(self, linux_params):
        # 文件上传
        LinuxBase(linux_params).sftp_upload_file('{}oracle_profile'.format(self.local_path), '/tmp/oracle_profile')
        LinuxBase(linux_params).sftp_upload_file('{}compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm'.format(self.local_path),
                                                 '/tmp/compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm')
        LinuxBase(linux_params).sftp_upload_file('{}97-oracle-database-sysctl.conf'.format(self.local_path),
                                                 '/tmp/97-oracle-database-sysctl.conf')
        LinuxBase(linux_params).sftp_upload_file('{}oracle-database-preinstall-19c.conf'.format(os.getcwd() + '/utils/oracle_onenode_install/'),
                                                 '/tmp/oracle-database-preinstall-19c.conf')
    
    def get_shm_config(self):
        memtotal = get_memtotal(self.node_info['node_ip'],self.node_info['node_password'])
        # 物理内存-1G 单位为字节
        shmmax = (float(memtotal)/1024/1024-1)*1024*1024*1024
        # 物理内存-1G 单位为page 
        shmall = (float(memtotal)/1024/1024-1)*1024*1024/4
        return (int(shmmax),int(shmall))

    def linux_config(self):
        cmd_list = []

        # 修改/etc/hosts信息
        ip_conf = "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n" \
                  "::1         localhost localhost.localdomain localhost6 localhost6.localdomain6\n" \
                  "{}  {}\n".format(self.node_info['node_ip'], self.node_info['hostname'])
        cmd_list.extend([
            'cat /dev/null > /etc/hosts',
            'echo "{}" > /etc/hosts'.format(ip_conf)
        ])
        # 禁用防火墙
        cmd_list.extend([
            'systemctl stop firewalld',
            'systemctl disable firewalld',
            "sed -i 's/SELINUX=enabled/SELINUX=disabled/g' /etc/selinux/config "
        ])
        # 禁用ntp服务

        # 创建组、用户
        group_list = ['groupdel {}'.format(group[1]) for group in self.linux_group_list] + \
                     ['groupadd -g {} {}'.format(group[0], group[1]) for group in self.linux_group_list]
        cmd_list.extend(group_list)
        cmd_list.extend([
            'userdel -rf oracle',
            'useradd -u {} -g oinstall -G dba,oper oracle'.format(
                self.linux_user_list['oracle']),
            "echo 'oracle:oracle'|chpasswd"
        ])

        # 创建目录,授权
        cmd_list.extend([
            'rm -rf /u01',
            'mkdir -p /u01/app/oracle/product/19.0.0/dbhome_1/',
            'mkdir -p /u01/app/oraInventory',
            'chown -R oracle:oinstall /u01/app/oracle',
            'chown -R oracle:oinstall /u01/app/oraInventory',
            'chmod -R 775 /u01/'
        ])

        # yum安装必需包
        cmd_list.extend([
            'yum -y install {}'.format(self.linux_packages),
            'rpm -ivh /tmp/compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm'
        ])

        # 内核参数设置
        shmmax,shmall = self.get_shm_config()
        cmd_list.extend([
            'mv /tmp/97-oracle-database-sysctl.conf /etc/sysctl.d/97-oracle-database-sysctl.conf',
            "sed -i 's/NODE_SHMMAX/{}/g' /etc/sysctl.d/97-oracle-database-sysctl.conf".format(shmmax),
            "sed -i 's/NODE_SHMALL/{}/g' /etc/sysctl.d/97-oracle-database-sysctl.conf".format(shmall),
            '/sbin/sysctl --system',
            '/sbin/sysctl -a'
        ])
        # 资源限制设置
        cmd_list.extend([
            'mv /tmp/oracle-database-preinstall-19c.conf /etc/security/limits.d/oracle-database-preinstall-19c.conf'
        ])

        # 执行runfixup脚本
        # cmd_list.extend([
        #     'sh /tmp/runfixup.sh'
        # ])

        return cmd_list

    def do_linux_config(self):
        self.log('开始进行linux基础配置..')
        self.log('{} {}：开始进行linux操作系统配置！'.format(self.node_info['node_ip'], self.node_info['hostname']))
        cmd_list = self.linux_config()

        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'root',
            'password': self.node_info['node_password']
        }
        linux_conn, _ = LinuxBase(linux_params).connection()

        self.upload_software(linux_params)

        # 修改主机名
        cmd_list.extend([
            'hostnamectl set-hostname {}'.format(self.node_info['hostname'])
        ])

        # 修改profile文件(需单独处理)
        cmd_list.extend([
            'mv /tmp/oracle_profile /home/oracle/.bash_profile',
            'chown oracle:oinstall /home/oracle/.bash_profile',
            "sed -i 's/NODE_ORACLE_SID/{}/g' /home/oracle/.bash_profile".format(
                self.node_info['dbname'])
        ])

        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('{} {}：linux操作系统配置完成'.format(self.node_info['node_ip'], self.node_info['hostname']))

        self.log('linux基础配置完成！')

    def oracle_execute_scripts(self):
        cmd = '/u01/app/oracle/product/19.0.0/dbhome_1/root.sh'
        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'root',
            'password': self.node_info['node_password']
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        LinuxBase(linux_params).exec_command_res(cmd)

    def oracle_install(self):
        self.log('开始进行oracle软件安装..')
        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'oracle',
            'password': 'oracle'
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        self.log('{} {}：开始上传oracle安装包..'.format(self.node_info['node_ip'], self.node_info['hostname']))
        LinuxBase(linux_params).sftp_upload_file('{}LINUX.X64_193000_db_home.zip'.format(self.local_path),'/tmp/LINUX.X64_193000_db_home.zip')
        self.log('oracle安装包上传完成！')
        self.log('开始解压缩oracle安装包..')
        cmd = 'unzip -q -o /tmp/LINUX.X64_193000_db_home.zip -d /u01/app/oracle/product/19.0.0/dbhome_1/'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('oracle安装包解压缩完成！')
        cmd = 'rm -f /tmp/LINUX.X64_193000_db_home.zip'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('oracle安装包清理完成！')

        self.log('开始生成oracle安装响应文件..')
        LinuxBase(linux_params).sftp_upload_file('{}db_install_onenode.rsp'.format(os.getcwd() + '/utils/oracle_onenode_install/'), '/tmp/db_install.rsp')
        self.log('oracle安装响应文件生成完成！')

        self.log('oracle软件安装前配置成功，请在节点{}上使用oracle用户执行静默安装脚本：'
                 '/u01/app/oracle/product/19.0.0/dbhome_1/runInstaller -silent -ignorePrereqFailure -responsefile /tmp/db_install.rsp '
                 ' 并根据提示执行后续脚本'.format(self.node_info['node_ip']))

        # 执行静默安装
        # self.log('开始Oracle软件静默安装,请关注{}：/tmp/oraclesetup.log'.format(node[ip]))
        # cmd = '/u01/app/oracle/product/19.0.0/dbhome_1/runInstaller -silent -ignorePrereqFailure -responsefile /tmp/db_install.rsp >/tmp/oraclesetup.log'
        # LinuxBase(linux_params).exec_command_res(cmd)
        # self.log('Oracle软件静默安装完成！')
        # self.log('请根据/tmp/oraclesetup.log中的提示执行脚本！')

        # 执行root脚本
        # self.oracle_execute_scripts()

    def oracle_dbca(self):
        self.log('开始进行dbca建库..')

        oracle_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'oracle',
            'password': 'oracle'
        }
        linux_conn, _ = LinuxBase(oracle_params).connection()

        self.log('开始生成dbca建库响应文件..')
        LinuxBase(oracle_params).sftp_upload_file('{}dbca_onenode.rsp'.format(os.getcwd() + '/utils/oracle_onenode_install/'), '/tmp/dbca.rsp')

        # 修改响应文件
        cmd_list = [
            "sed -i 's/NODE_DBNAME/{}/g' /tmp/dbca.rsp".format(self.node_info['dbname']),
            "sed -i 's/NODE_PDBNAME/{}/g' /tmp/dbca.rsp".format(self.node_info['pdbname'])
        ]
        res = [LinuxBase(oracle_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('dbca建库响应文件生成完成！')

        self.log('dbca配置成功，请在节点{}上使用oracle用户执行dbca建库脚本：/u01/app/oracle/product/19.0.0/dbhome_1/bin/dbca -silent -createDatabase -ignorePrereqFailure '
                 '-responseFile /tmp/dbca.rsp'
                 ' 并根据提示执行后续脚本'.format(self.node_info['node_ip']))
                 
        self.log('DBCA建库成功后，创建数据库监听：netca -silent -responsefile /u01/app/oracle/product/19.0.0/dbhome_1/assistants/netca/netca.rsp')

        # 开始静默安装
        # self.log('开始进行dbca静默安装，请关注{}：/tmp/dbca.log'.format(node['ip']))
        # cmd = '/u01/app/oracle/product/19.0.0/dbhome_1/bin/dbca -silent -createDatabase -ignorePrereqFailure ' \
        #       '-responseFile /tmp/dbca.rsp > /tmp/dbca.log'
        # LinuxBase(oracle_params).exec_command_res(cmd)
        # self.log('dbca静默安装完成..')

    def do_onenode_install(self,module):
        if module == 'linux':
            self.log('linux基础配置已启动..')
            self.clear_log()
            self.do_linux_config()
        elif module == 'oracle':
            self.log('oracle安装已启动..')
            self.oracle_install()
        elif module =='dbca':
            self.log('dbca建库已启动..')
            self.oracle_dbca()
        elif module == 'clear':
            self.log('开始清理Oracle安装..')
            self.clear_rac()
        else:
            print('输入参数不合法！')

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

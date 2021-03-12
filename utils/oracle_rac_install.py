# encoding： utf-8

from utils.linux_base import LinuxBase
from utils.tools import now_local
from utils.tools import mysql_exec,mysql_query,now,get_memtotal
import os

class OracleRacInstall():
    def __init__(self, rac_info, node_list):
        self.rac_info = rac_info
        self.node_list = node_list
        self.linux_group_list = [
            [5000, 'asmadmin'],
            [5001, 'asmdba'],
            [5002, 'asmoper'],
            [5003, 'dba'],
            [5004, 'oper'],
            [5005, 'backupdba'],
            [5006, 'dgdba'],
            [5007, 'kmdba'],
            [5008, 'racdba'],
            [5009, 'oinstall']
        ]
        self.linux_user_list = {
            'grid': 5010,
            'oracle': 5011
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
        log_type = 'Oracle RAC安装'
        current_time = now_local()
        print('{}: {}'.format(current_time,log_content))
        sql = "insert into setup_log(log_type,log_time,log_level,log_content)" \
              "values(%s,%s,%s,%s)"
        values = (log_type,current_time,log_level,log_content)
        mysql_exec(sql, values)

    def clear_rac(self):
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
            ['userdel -rf grid',
            'userdel -rf oracle'],
        )
        # 清除ASM信息
        cmd_list.extend(
            ['dd if=/dev/zero of={} bs=8192 count=2147'.format(self.rac_info['ocr_disk']),
            'dd if=/dev/zero of={} bs=8192 count=2147'.format(self.rac_info['data_disk'])]
        )
        # 清理完成后重启服务器
        cmd_list.extend(
            ['reboot']
        )
        for node in node_list:
            linux_params = {
                'hostname': node['ip'],
                'port': 22,
                'username': 'root',
                'password': node['password']
            }
            linux_conn, _ = LinuxBase(linux_params).connection()
            self.log('{}：开始清理Oracle RAC！'.format(node['ip']))
            res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
            self.log('Oracle RAC清理完成！')


    def upload_software(self, linux_params):
        # 文件上传
        LinuxBase(linux_params).sftp_upload_file('{}grid_profile'.format(self.local_path), '/tmp/grid_profile')
        LinuxBase(linux_params).sftp_upload_file('{}oracle_profile'.format(self.local_path), '/tmp/oracle_profile')
        LinuxBase(linux_params).sftp_upload_file('{}compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm'.format(self.local_path),
                                                 '/tmp/compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm')
        LinuxBase(linux_params).sftp_upload_file('{}cvuqdisk-1.0.10-1.rpm'.format(self.local_path),
                                                 '/tmp/cvuqdisk-1.0.10-1.rpm')
        LinuxBase(linux_params).sftp_upload_file('{}97-oracle-database-sysctl.conf'.format(self.local_path),
                                                 '/tmp/97-oracle-database-sysctl.conf')
        LinuxBase(linux_params).sftp_upload_file('{}oracle-database-preinstall-19c.conf'.format(self.local_path),
                                                 '/tmp/oracle-database-preinstall-19c.conf')

    def get_shm_config(self,node1):
        memtotal = get_memtotal(node1['ip'],node1['password'])
        # 物理内存-1G 单位为字节
        shmmax = (float(memtotal)/1024/1024-1)*1024*1024*1024
        # 物理内存-1G 单位为page 
        shmall = (float(memtotal)/1024/1024-1)*1024*1024/4
        return (int(shmmax),int(shmall))

    def linux_config(self, node1, node2):
        cmd_list = []

        # 修改/etc/hosts信息
        ip_conf = "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n" \
                  "::1         localhost localhost.localdomain localhost6 localhost6.localdomain6\n" \
                  "{}  {}\n" \
                  "{}  {}\n" \
                  "{}  {}-vip\n" \
                  "{}  {}-vip\n" \
                  "{}  {}-priv\n" \
                  "{}  {}-priv\n" \
                  "{}  {}-cluster   {}-cluster-scan".format(node1['ip'], self.rac_info['hostname'] + node1['node_id'],
                                                            node2['ip'], self.rac_info['hostname'] + node2['node_id'],
                                                            node1['ip_vip'], self.rac_info['hostname'] + node1['node_id'],
                                                            node2['ip_vip'], self.rac_info['hostname'] + node2['node_id'],
                                                            node1['ip_priv'], self.rac_info['hostname'] + node1['node_id'],
                                                            node2['ip_priv'], self.rac_info['hostname'] + node2['node_id'],
                                                            self.rac_info['scan_ip'], self.rac_info['hostname'],
                                                            self.rac_info['hostname'])
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
            'userdel -rf grid',
            'userdel -rf oracle',
            'useradd -u {} -g oinstall -G asmadmin,asmdba,racdba,asmoper grid'.format(self.linux_user_list['grid']),
            'useradd -u 5011 -g oinstall -G dba,asmdba,backupdba,dgdba,kmdba,racdba,oper oracle'.format(
                self.linux_user_list['oracle']),
            "echo 'grid:oracle'|chpasswd",
            "echo 'oracle:oracle'|chpasswd"
        ])

        # 创建目录,授权
        cmd_list.extend([
            'rm -rf /u01',
            'mkdir -p /u01/app/19.0.0/grid',
            'mkdir -p /u01/app/grid',
            'mkdir -p /u01/app/oracle/product/19.0.0/dbhome_1/',
            'mkdir -p /u01/app/oraInventory',
            'chown -R grid:oinstall /u01',
            'chown -R oracle:oinstall /u01/app/oracle',
            'chmod -R 775 /u01/'
        ])

        # yum安装必需包
        cmd_list.extend([
            'yum -y install {}'.format(self.linux_packages),
            'rpm -ivh /tmp/compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm',
            'rpm -ivh /tmp/cvuqdisk-1.0.10-1.rpm'
        ])

        # 内核参数设置
        shmmax,shmall = self.get_shm_config(node1)
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

        # 关闭avahi-daemon服务
        cmd_list.extend([
            'systemctl stop avahi-daemon.socket',
            'systemctl stop avahi-daemon.service',
            'systemctl disable avahi-daemon.socket',
            'systemctl disable avahi-daemon.service'
            ]
        )

        return cmd_list

    def do_linux_config(self, node1, node2):
        self.log('开始进行linux基础配置..')
        for node in self.node_list:
            self.log('{} {}：开始进行linux操作系统配置！'.format(node['ip'], node['hostname']))
            cmd_list = self.linux_config(node1, node2)

            linux_params = {
                'hostname': node['ip'],
                'port': 22,
                'username': 'root',
                'password': node['password']
            }
            linux_conn, _ = LinuxBase(linux_params).connection()

            self.upload_software(linux_params)

            # 修改主机名
            cmd_list.extend([
                'hostnamectl set-hostname {}'.format(self.rac_info['hostname'] + node['node_id'])
            ])

            # 修改profile文件(需单独处理)
            cmd_list.extend([
                'mv /tmp/grid_profile /home/grid/.bash_profile',
                'chown grid:oinstall /home/grid/.bash_profile',
                "sed -i 's/NODE_ASM_SID/{}/g' /home/grid/.bash_profile".format('+ASM' + node['node_id']),
                'mv /tmp/oracle_profile /home/oracle/.bash_profile',
                'chown oracle:oinstall /home/oracle/.bash_profile',
                "sed -i 's/NODE_ORACLE_SID/{}/g' /home/oracle/.bash_profile".format(
                    self.rac_info['dbname'] + node['node_id'])
            ])

            res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
            self.log('{} {}：linux操作系统配置完成'.format(node['ip'], node['hostname']))
        self.log('所有节点linux基础配置完成！')

    def grid_execute_scripts(self):

        for node in self.node_list:
            cmd = '/u01/app/oraInventory/orainstRoot.sh'
            linux_params = {
                'hostname': node['ip'],
                'port': 22,
                'username': 'root',
                'password': node['password']
            }
            linux_conn, _ = LinuxBase(linux_params).connection()
            LinuxBase(linux_params).exec_command_res(cmd)

        for node in self.node_list:
            cmd = '/u01/app/19.0.0/grid/root.sh'
            linux_params = {
                'hostname': node['ip'],
                'port': 22,
                'username': 'root',
                'password': node['password']
            }
            linux_conn, _ = LinuxBase(linux_params).connection()
            LinuxBase(linux_params).exec_command_res(cmd)

    def grid_install(self, node):
        self.log('开始进行grid集群软件安装..')
        # 只在第一节点操作
        linux_params = {
            'hostname': node['ip'],
            'port': 22,
            'username': 'grid',
            'password': 'oracle'
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        # 上传grid安装包
        self.log('{} {}：开始上传grid安装包..'.format(node['ip'], node['hostname']))
        LinuxBase(linux_params).sftp_upload_file('{}LINUX.X64_193000_grid_home.zip'.format(self.local_path), '/tmp/LINUX.X64_193000_grid_home.zip')
        self.log('grid安装包上传完成！')

        self.log('{} {}：开始解压缩grid安装包！'.format(node['ip'], node['hostname']))
        cmd = 'unzip -q -o /tmp/LINUX.X64_193000_grid_home.zip -d /u01/app/19.0.0/grid/'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('grid安装包解压缩完成！')
        cmd = 'rm -f /tmp/LINUX.X64_193000_grid_home.zip'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('grid安装包清理完成！')

        self.log('开始节点间grid用户ssh互信配置..')
        LinuxBase(linux_params).sftp_upload_file('{}auto_ssh.sh'.format(self.local_path), '/tmp/auto_ssh.sh')
        self.log('ssh互信配置脚本上传完成！')

        # 配置grid用户ssh互信
        cmd_list = [
            'rm -f /tmp/hostlist.cfg',
            'echo {} > /tmp/hostlist.cfg' .format(self.rac_info['hostname']+'1'),
            'echo {} >> /tmp/hostlist.cfg' .format(self.rac_info['hostname']+'2'),
            'sh /tmp/auto_ssh.sh grid oracle /tmp/hostlist.cfg'
            ]
        res = [LinuxBase(linux_params).exec_command_res(cmd) for cmd in cmd_list]
        self.log('grid用户ssh互信配置完成！')

        self.log('开始生成grid安装响应文件..')
        LinuxBase(linux_params).sftp_upload_file('{}gridsetup.rsp'.format(self.local_path), '/tmp/gridsetup.rsp')

        # 修改响应文件
        cmd_list = [
            "sed -i 's/NODE_HOSTNAME/{}/g' /tmp/gridsetup.rsp".format(self.rac_info['hostname']),
            "sed -i 's/NODE_PUBLIC_INTERFACE/{}/g' /tmp/gridsetup.rsp".format(self.rac_info['public_interface']),
            "sed -i 's/NODE_PUBLIC_SUBNET/{}/g' /tmp/gridsetup.rsp".format(self.rac_info['public_subnet']),
            "sed -i 's/NODE_PRIVATE_INTERFACE/{}/g' /tmp/gridsetup.rsp".format(self.rac_info['private_interface']),
            "sed -i 's/NODE_PRIVATE_SUBNET/{}/g' /tmp/gridsetup.rsp".format(self.rac_info['private_subnet']),
            "sed -i 's#NODE_OCR_DISK#{}#g' /tmp/gridsetup.rsp".format(self.rac_info['ocr_disk']),
            "sed -i 's#NODE_OCR_PATH#{}#g' /tmp/gridsetup.rsp".format(self.rac_info['disk_path'])
        ]
        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('grid安装响应文件生成完成！')

        # 先决条件检查
        # $ORACLE_HOME/runcluvfy.sh stage -pre crsinst -responseFile gridsetup.rsp
        self.log('grid集群配置成功，请在1号节点{}上使用grid用户执行先决条件检查：$ORACLE_HOME/runcluvfy.sh stage -pre crsinst -responseFile /tmp/gridsetup.rsp'.format(node['ip']))

        self.log('在先决条件检查完成后，请在1号节点{}上执行静默安装：/u01/app/19.0.0/grid/gridSetup.sh -silent -ignorePrereqFailure -responseFile /tmp/gridsetup.rsp'
                 ' 并根据提示执行root.sh脚本'.format(node['ip']))

        # 执行静默安装
        # self.log('开始执行集群软件静默安装..请关注grid安装日志 {}：/tmp/gridsetup.log'.format(node['ip']))
        # cmd = '/u01/app/19.0.0/grid/gridSetup.sh -silent -ignorePrereqFailure -responseFile /tmp/gridsetup.rsp > /tmp/gridsetup.log'
        # LinuxBase(linux_params).exec_command_res(cmd)
        # self.log('grid集群件静默安装完成！')
        # self.log('请根据/tmp/gridsetup.log中的提示执行脚本！')
        # 执行静默安装脚本
        # self.grid_execute_scripts()

        # 执行配置工具脚本
        cmd = '/u01/app/19.0.0/grid/gridSetup.sh -executeConfigTools -responseFile /tmp/gridsetup.rsp -silent'
        # LinuxBase(linux_params).exec_command_res(cmd)

        # 安装后进行检查
        # $ORACLE_HOME/runcluvfy.sh  stage -post  crsinst -n "cispdb1,cispdb2"  -verbose

    def oracle_execute_scripts(self):
        for node in self.node_list:
            cmd = '/u01/app/oracle/product/19.0.0/dbhome_1/root.sh'
            linux_params = {
                'hostname': node['ip'],
                'port': 22,
                'username': 'root',
                'password': node['password']
            }
            linux_conn, _ = LinuxBase(linux_params).connection()
            LinuxBase(linux_params).exec_command_res(cmd)


    def oracle_install(self, node):
        self.log('开始进行oracle软件安装..')
        linux_params = {
            'hostname': node['ip'],
            'port': 22,
            'username': 'oracle',
            'password': 'oracle'
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        self.log('{} {}：开始上传oracle安装包..'.format(node['ip'], node['hostname']))
        LinuxBase(linux_params).sftp_upload_file('{}LINUX.X64_193000_db_home.zip'.format(self.local_path),'/tmp/LINUX.X64_193000_db_home.zip')
        self.log('oracle安装包上传完成！')
        self.log('开始解压缩oracle安装包..')
        cmd = 'unzip -q -o /tmp/LINUX.X64_193000_db_home.zip -d /u01/app/oracle/product/19.0.0/dbhome_1/'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('oracle安装包解压缩完成！')
        cmd = 'rm -f /tmp/LINUX.X64_193000_db_home.zip'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('oracle安装包清理完成！')

        # 配置oracle用户ssh互信
        self.log('开始节点间oracle用户ssh互信配置..')
        cmd_list = [
            'rm -f /tmp/hostlist.cfg',
            'echo {} > /tmp/hostlist.cfg'.format(self.rac_info['hostname'] + '1'),
            'echo {} >> /tmp/hostlist.cfg'.format(self.rac_info['hostname'] + '2'),
            'sh /tmp/auto_ssh.sh oracle oracle /tmp/hostlist.cfg'
        ]
        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('oracle用户ssh互信配置完成！')

        self.log('开始生成oracle安装响应文件..')
        LinuxBase(linux_params).sftp_upload_file('{}db_install.rsp'.format(self.local_path), '/tmp/db_install.rsp')

        # 修改响应文件
        cmd_list = [
            "sed -i 's/NODE_HOSTNAME/{}/g' /tmp/db_install.rsp".format(self.rac_info['hostname']),
        ]
        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('oracle安装响应文件生成完成！')

        self.log('oracle软件安装前配置成功，请在1号节点{}上使用oracle用户执行静默安装脚本：'
                 '/u01/app/oracle/product/19.0.0/dbhome_1/runInstaller -silent -ignorePrereqFailure -responsefile /tmp/db_install.rsp '
                 ' 并根据提示执行后续脚本'.format(node['ip']))

        # 执行静默安装
        # self.log('开始Oracle软件静默安装,请关注{}：/tmp/oraclesetup.log'.format(node[ip]))
        # cmd = '/u01/app/oracle/product/19.0.0/dbhome_1/runInstaller -silent -ignorePrereqFailure -responsefile /tmp/db_install.rsp >/tmp/oraclesetup.log'
        # LinuxBase(linux_params).exec_command_res(cmd)
        # self.log('Oracle软件静默安装完成！')
        # self.log('请根据/tmp/oraclesetup.log中的提示执行脚本！')

        # 执行root脚本
        # self.oracle_execute_scripts()

    def oracle_dbca(self,node):
        self.log('开始进行dbca建库..')
        grid_params = {
            'hostname': node['ip'],
            'port': 22,
            'username': 'grid',
            'password': 'oracle'
        }
        self.log('开始创建ASM磁盘组：DATA..')
        # 创建ASM磁盘组
        cmd = "/u01/app/19.0.0/grid/bin/asmca -silent -createDiskGroup -diskGroupName DATA -disk '{}' " \
              "-redundancy EXTERNAL -au_size 4 -compatible.asm '19.0.0.0.0' " \
              "-compatible.rdbms '19.0.0.0.0' -compatible.advm '19.0.0.0.0'".format(self.rac_info['data_disk'])

        LinuxBase(grid_params).exec_command_res(cmd)
        self.log('ASM磁盘组创建完成！')

        oracle_params = {
            'hostname': node['ip'],
            'port': 22,
            'username': 'oracle',
            'password': 'oracle'
        }
        linux_conn, _ = LinuxBase(oracle_params).connection()

        self.log('开始生成dbca建库响应文件..')
        LinuxBase(oracle_params).sftp_upload_file('{}dbca.rsp'.format(self.local_path), '/tmp/dbca.rsp')

        # 修改响应文件
        cmd_list = [
            "sed -i 's/NODE_HOSTNAME/{}/g' /tmp/dbca.rsp".format(self.rac_info['hostname']),
            "sed -i 's/NODE_DBNAME/{}/g' /tmp/dbca.rsp".format(self.rac_info['dbname']),
            "sed -i 's/NODE_PDBNAME/{}/g' /tmp/dbca.rsp".format(self.rac_info['pdbname'])
        ]
        res = [LinuxBase(oracle_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('dbca建库响应文件生成完成！')

        self.log('dbca配置成功，请在1号节点{}上使用oracle用户执行dbca建库脚本：/u01/app/oracle/product/19.0.0/dbhome_1/bin/dbca -silent -createDatabase -ignorePrereqFailure '
                 '-responseFile /tmp/dbca.rsp'
                 ' 并根据提示执行后续脚本'.format(node['ip']))

        # 开始静默安装
        # self.log('开始进行dbca静默安装，请关注{}：/tmp/dbca.log'.format(node['ip']))
        # cmd = '/u01/app/oracle/product/19.0.0/dbhome_1/bin/dbca -silent -createDatabase -ignorePrereqFailure ' \
        #       '-responseFile /tmp/dbca.rsp > /tmp/dbca.log'
        # LinuxBase(oracle_params).exec_command_res(cmd)
        # self.log('dbca静默安装完成..')

    def do_rac_install(self,module):
        node1 = self.node_list[0] if self.node_list[0]['node_id'] == '1' else self.node_list[1]
        node2 = self.node_list[1] if self.node_list[0]['node_id'] == '1' else self.node_list[0]
        if module == 'linux':
            self.log('linux基础配置已启动..')
            self.clear_log()
            self.do_linux_config(node1, node2)
        elif module == 'rac':
            self.log('grid安装已启动..')
            self.grid_install(node1)
        elif module == 'oracle':
            self.log('oracle安装已启动..')
            self.oracle_install(node1)
        elif module =='dbca':
            self.log('dbca建库已启动..')
            self.oracle_dbca(node1)
        elif module == 'clear':
            self.log('开始清理Oracle rac..')
            self.clear_rac()
        else:
            print('输入参数不合法！')

if __name__ == '__main__':
    rac_info = {
        'dbname': 'cispcdb',
        'pdbname': 'cisp',
        'scan_ip': '192.168.48.55',
        'hostname': 'cispdb',
        'soft_path': '/',
        'public_interface': 'ens32',
        'public_subnet': '192.168.48.0',
        'private_interface': 'ens35',
        'private_subnet': '10.10.10.0',
        'ocr_disk': '/dev/mapper/asm-ocr',
        'disk_path': '/dev/mapper/asm*',
        'data_disk' : '/dev/mapper/asm-data'
    }
    node_list = [
        {
            'node_id': '1',
            'hostname': rac_info['hostname'] + '1',
            'ip': '192.168.48.51',
            'ip_vip': '192.168.48.53',
            'ip_priv': '10.10.10.101',
            'password': 'oracle'},
        {
            'node_id': '2',
            'hostname': rac_info['hostname'] + '2',
            'ip': '192.168.48.52',
            'ip_vip': '192.168.48.54',
            'ip_priv': '10.10.10.102',
            'password': 'oracle'}
    ]

    oracleracinstall = OracleRacInstall(rac_info, node_list)
    oracleracinstall.do_rac_install('clear')

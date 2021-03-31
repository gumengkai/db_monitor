#! /usr/bin/python
# encoding:utf-8

import paramiko
import re
import os
from collections import defaultdict
from utils.linux_base import LinuxBase
import timeout_decorator

stat_file_config = {
    'cpu': '/proc/stat',
    'net': '/proc/net/dev',
    'io': '/proc/diskstats',
    'mem': '/proc/meminfo',
    'sys': '/proc/stat',
    'vm': '/proc/vmstat',
    'load': '/proc/loadavg',
    'uptime': '/proc/uptime',
    'tcp': '/proc/net/tcp',
    'tcp6': '/proc/net/tcp6'
}

IGNORE_FS = set(['binfmt_misc', 'cgroup', 'debugfs', 'devpts', 'devtmpfs',
                 'fusectl', 'proc', 'pstore', 'securityfs',
                 'sysfs', 'tmpfs', 'xenfs', 'iso9660'])

import time

def format_stat(label, stat_vals):
    ret = {}
    for i in range(len(label)):
        if ':' in label[i]:
            label_n, idx = label[i].split(':')
            idx = int(idx)
        else:
            label_n, idx = label[i], i

        ret[label_n] = round(stat_vals[i], 2)

    return ret


class LinuxStat(LinuxBase):
    def __init__(self,params,conn):
        super().__init__(params)
        self.params = params
        self.conn = conn
        self.curr_stat = {}
        self.stat = {}
        self.last_time = time.time()
        self.loop_cnt = 0
        self.old_stat = {
            'cpu': tuple(0 for _ in range(5)),
            'io': tuple(0 for _ in range(11)),
            'sys': tuple(0 for _ in range(6)),
            'vm': tuple(0 for _ in range(6))
        }

    @timeout_decorator.timeout(60)
    def get_linux(self):
        # init net data
        net_nics = self.get_net_nics()
        for nic in net_nics:
            self.old_stat['net_' + nic] = (0,0)
        # init block disk data
        self.block_devices = self.get_block_devices()
        for disk in self.block_devices:
            self.old_stat['io_' + disk] = tuple(0 for _ in range(11))
        #
        self.old_stat['vm'] = tuple(0 for _ in range(6))
        # get stat 1
        stat1 = self.get_linux_stat()
        # get stat 2
        stat2 = self.get_linux_stat()
        return stat2

    def get_host_info(self):
        # get_hostname mysql50
        command = 'hostname'
        res = super().exec_command(command,self.conn)
        hostname = res.readlines()[0]
        # get ostype,version,frame Linux 2.6.32-431.el6.x86_64
        command = 'uname -a'
        res = super().exec_command(command,self.conn)
        res =  res.readlines()[0]
        ostype = res.split(' ')[0]
        kernel = res.split(' ')[2]
        frame = res.split(' ')[11]
        # linux version
        linux_version = ''
        command = 'cat /etc/redhat-release'
        res = super().exec_command(command,self.conn)
        linux_version = res.readlines()[0]
        # print(linux_version)
        # up days
        uptime = self.get_uptime()
        up_days = round(float(uptime) / 60 / 60 / 24, 2)

        return {
            'hostname': hostname,
            'ostype': ostype,
            'kernel': kernel,
            'frame': frame,
            'linux_version':linux_version,
            'updays':up_days
        }

    def get_cpu_info(self):
        cpu_set = set()
        counter = defaultdict(int)
        counter_cpu_mode = defaultdict(int)
        counter_cache_size = defaultdict(int)
        counter_cpu_speed = defaultdict(int)
        cpu_cores = 0

        command = 'cat /proc/cpuinfo'
        res = super().exec_command(command,self.conn)
        res = res.readlines()

        for line in res:
            if line.startswith('physical id'):
                cpu_set.add(line)
            elif line.startswith('cache size'):
                cache_size = line.split(':')[1].strip()
                counter_cache_size[cache_size] += 1
            elif line.startswith('processor'):
                counter['virtual'] += 1
            elif line.startswith('model name'):
                model_name = line.split(':')[1].strip()
                counter_cpu_mode[model_name] += 1
            elif line.startswith('cpu MHz'):
                cpu_hz = line.split(':')[1].strip()
                counter_cpu_speed[cpu_hz] += 1
            elif line.startswith('cpu cores'):
                cpu_cores = int(line.split(':')[1].strip())

        num_processor = len(cpu_set)
        virtual = counter['virtual']
        if num_processor == 0:
            num_processor = virtual

        cpu_cores = cpu_cores * num_processor

        speeds = []
        for speed, num in counter_cpu_speed.items():
            speeds.append('%dx%s' % (num, speed))

        cpu_speed = ", ".join(speeds)

        models = []
        for model, num in counter_cpu_mode.items():
            models.append('%dx%s' % (num, model))

        cpu_mode = ", ".join(models)

        caches = []
        for cache, num in counter_cache_size.items():
            caches.append('%dx%s' % (num, cache))

        cpu_cache = ", ".join(caches)

        processor = "pyhsical = %d, cores = %d, virtual cpu = %d" % (num_processor, cpu_cores, virtual)

        # return (processor, cpu_speed, cpu_mode, cpu_cache, virtual)
        return {
            'processor': processor,
            'cpu_speed': cpu_speed,
            'cpu_mode': cpu_mode,
            'cpu_cache': cpu_cache,
            'virtual':virtual
        }

    def get_memtotal(self):
        command = 'cat /proc/meminfo'
        res = super().exec_command(command,self.conn)
        res =  res.readlines()
        memtotal = 0
        for line in res:
            if line.startswith('MemTotal'):
                memtotal = line.split()[1]
        # 单位为KB
        return {
            'memtotal': memtotal
        }

    def get_host_ip(self):
        ip_list = []
        command = 'ifconfig'
        res = super().exec_command(command,self.conn)
        res =  res.readlines()
        for line in res:
            if line.strip().startswith('inet') and not line.strip().startswith('inet6'):
                ip_addr =  line.strip().split(' ')[1]
                if ip_addr.startswith('addr'):
                    ip = ip_addr.split(':')[1]
                else:
                    ip = ip_addr
                if ip != '127.0.0.1' and ip.startswith(''):
                    ip_list.append(ip)
        ipinfo =  ','.join(ip_list)
        return {
            'ipinfo':ipinfo
        }


    def get_linux_stat(self):
        curr_time = time.time()
        if self.loop_cnt == 0:
            elapsed = self.get_uptime()
        else:
            elapsed = curr_time - self.last_time

        #get all status
        linux_stat = {}

        # get hostconf
        linux_stat['hostinfo'] = self.get_host_info()
        linux_stat['cpuinfo'] = self.get_cpu_info()
        linux_stat['Memtotal'] = self.get_memtotal()
        linux_stat['ipinfo'] = self.get_host_ip()

        linux_stat['load'] = self.get_load()
        linux_stat['cpu'] = self.get_cpu_stat()
        linux_stat['iostat'] = self.get_io_stat(elapsed)
        linux_stat['mem'] = self.get_mem_stat()
        linux_stat['vmstat'] = self.get_vm_stat(elapsed)
        linux_stat['tcpstat'] = self.get_tcp_conn_stat()
        linux_stat['net'] = self.get_net_stat(elapsed)
        linux_stat['proc'] = self.get_proc_stat(elapsed)
        linux_stat['hostinfo'] = self.get_host_info()

        # update timestamp
        self.last_time = curr_time
        self.loop_cnt += 1
        return linux_stat


    def get_cpu_stat(self):
        #usr, sys, idle, iowait, steal
        stat_name = 'cpu'
        for l in self.get_stat(stat_name):
            if l[0] == 'cpu' and len(l) >= 9:
                self.curr_stat[stat_name] = (int(l[1]) + int(l[2]) + int(l[6]) + int(l[7]),
                                             int(l[3]), int(l[4]), int(l[5]), int(l[8]))

        stat_old = self.old_stat[stat_name]
        stat_curr = self.curr_stat[stat_name]

        delta = (sum(stat_curr) - sum(stat_old)) * 1.0
        if delta > 0:
            self.stat[stat_name] = tuple(100.0 * (stat_curr[i] - stat_old[i])/delta for i in range(5))
        else:
            self.stat[stat_name] = tuple(0 for _ in range(5))

        self.old_stat[stat_name] = stat_curr

        label = ('cpu_user', 'cpu_sys', 'cpu_idle', 'cpu_iowait')
        return format_stat(label, self.stat[stat_name])


    def get_vm_stat(self, elapsed):
        stat_name = 'vm'
        stats = {'pgpgin':0, 'pgpgout':1, 'pswpin':2, 'pswpout':3, 'pgfault':4, 'pgmjfault':5 }
        vm_stat = [0 for _ in range(6)]
        for l in self.get_stat(stat_name):
            if l[0] in stats:
                vm_stat[stats[l[0]]] = int(l[1])

        stat_old = self.old_stat[stat_name]

        self.stat[stat_name] = tuple((vm_stat[i] - stat_old[i])/elapsed for i in range(len(vm_stat)))
        self.old_stat[stat_name] = vm_stat

        label = ('pgin', 'pgout', 'swapin', 'swapout', 'pgfault', 'pgmjfault')
        return format_stat(label, self.stat[stat_name])

    def get_mem_stat(self):
        stat_name = 'mem'
        stats = {
            'MemTotal':0,
            'MemFree':1,
            'Buffers':2,
            'Cached':3,
            'SReclaimable':4,
            'Shmem':5,
            'SwapTotal':6,
            'SwapFree':7}
        #self.val['MemUsed'] = self.val['MemTotal'] - self.val['MemFree'] - self.val['Buffers'] - self.val['Cached'] - self.val['SReclaimable'] + self.val['Shmem']

        mem_stat = [0 for _ in range(8)]
        for l in self.get_stat(stat_name, ':'):
            if l[0] in stats:
                mem_stat[stats[l[0]]] = int(l[1])/1024

        mem_used = mem_stat[0] - mem_stat[1] - mem_stat[2] - mem_stat[3] - mem_stat[4] + mem_stat[5]
        swap_used = mem_stat[6] - mem_stat[7]

        #used, free, buff, cache, swap used, swap free
        self.stat[stat_name] = (mem_used, mem_stat[1], mem_stat[2], mem_stat[3], swap_used, mem_stat[7])
        label = ('mem_used_mb', 'mem_free', 'mem_buffer', 'mem_cache','swap_used','swap_free')
        return format_stat(label, self.stat[stat_name])

    def get_proc_stat(self, elapsed):
        stat_name = 'sys'
        stats = {'processes':0, 'procs_running':1, 'procs_blocked':2, 'intr':3, 'ctxt':4, 'softirq':5 }

        self.curr_stat[stat_name] = [0 for _ in range(6)]
        for l in self.get_stat(stat_name):
            if l[0] in stats:
                self.curr_stat[stat_name][stats[l[0]]] = int(l[1])

        val2 = self.curr_stat[stat_name]
        val1 = self.old_stat[stat_name]

        #proc_new, proc_running, proc_block, intrupts, ctx switchs, softirq
        self.stat[stat_name] = (1.0*(val2[0]-val1[0])/elapsed, val2[1], val2[2],
                           1.0*(val2[3]-val1[3])/elapsed, 1.0*(val2[4]-val1[4])/elapsed, 1.0*(val2[5]-val1[5])/elapsed)

        self.old_stat[stat_name] = val2
        label = ('proc_new', 'proc_running', 'proc_block', 'intr', 'ctx', 'softirq')
        return format_stat(label, self.stat[stat_name])

    def get_tcp_conn_stat(self):
        conn_listen, conn_esta, conn_syn, conn_wait, conn_close = 0,0,0,0,0
        for l in self.get_tcp_stat():
            if l[3] in set(['0A']): conn_listen += 1
            elif l[3] in set(['01']): conn_esta += 1
            elif l[3] in set(['02', '03', '09']): conn_syn += 1
            elif l[3] in set(['06']): conn_wait += 1
            elif l[3] in set(['04', '05', '07', '08', '0B']): conn_close += 1

        self.stat['tcp_conns'] = (conn_listen,conn_esta, conn_syn, conn_wait, conn_close)
        label = ('tcp_listen', 'tcp_connected', 'tcp_syn', 'tcp_timewait', 'tcp_close')
        return format_stat(label, self.stat['tcp_conns'])

    def get_tcp_stat(self):
        for l in self.get_stat('tcp'):
            yield l
        for l in self.get_stat('tcp6'):
            yield l

    def get_load(self):
        stat_name = 'load'
        for l in self.get_stat(stat_name):
            if len(l) < 3: continue
            self.stat[stat_name] = (float(l[0]), float(l[1]), float(l[2]))

        label = ('load1', 'load5', 'load15')
        return format_stat(label, self.stat[stat_name])

    def get_uptime(self):
        stat_name = 'uptime'
        for l in self.get_stat(stat_name):
            if len(l) < 2: continue
            uptime = float(l[0])
            self.curr_stat[stat_name] = (uptime,)
            return uptime

    def get_net_nics(self):
        command = 'cat /proc/net/dev'
        res = super().exec_command(command,self.conn)
        fd = res
        nic_filter = re.compile("^(lo|face|docker\d+)$")
        ret = []
        for line in fd.readlines():
            l = line.replace(':', ' ').split()
            if len(l) < 17 or nic_filter.match(l[0]):
                continue
            try:
                ret.append(l[0])
            except:
                pass
        return ret

    def get_mounted_dev(self):
        mounted_dev = set()
        command = 'cat /etc/mtab'
        res = super().exec_command(command,self.conn)
        f = res
        for i in f.readlines():
            # /dev/xvda1 / ext4 rw,errors=remount-ro 0 0
            s = i.split()
            if len(s) >= 4 and s[2] not in IGNORE_FS:
                dev = s[0]
                if dev.startswith('/dev/mapper'):
                    try:
                        dev = os.path.basename(os.readlink(dev))
                    except:
                        dev = None
                else:
                    # /dev/xvda1 => xvda
                    dev = re.sub('\d+$', '', os.path.basename(dev))

                if dev:
                    mounted_dev.add(dev)
        return mounted_dev

    def get_block_devices(self):
        disk_filter = re.compile('^(loop|ram|sr|asm)\d+$')
        ret = []
        mounted_dev = self.get_mounted_dev()
        command = 'ls -l /sys/block/*'
        res = super().exec_command(command,self.conn)
        fd = res
        for l in res.readlines():
            dev_name = l.split('/')[-1]
            dev_name = re.sub(':','',dev_name).strip()
            if disk_filter.match(dev_name):
                continue
            if dev_name in mounted_dev:
                ret.append(dev_name)
        return ret[:30]


    def get_net_stat(self, elapsed):
        stat_name = 'net'
        net_nics = self.get_net_nics()
        ret = []
        label = ('recv', 'send')
        for l in self.get_stat(stat_name,':'):
            if l[0] in net_nics and len(l) >= 17:
                stat_nic = '%s_%s' % (stat_name, l[0])
                #net recv, net send, kb
                stat_curr = (int(l[1]), int(l[9]))
                stat_old = self.old_stat[stat_nic]
                self.stat[stat_nic] = tuple(1.0*(stat_curr[i] - stat_old[i])/elapsed/1024 for i in range(2))
                self.old_stat[stat_nic] = stat_curr

                netstat = format_stat(label, self.stat[stat_nic])
                netstat['nic'] = l[0]
                ret.append(netstat)
        return ret

    def get_io_stat(self, elapsed):
        stat_name = 'io'
        self.curr_stat['io'] = tuple(0 for _ in range(11))
        ret = []

        num_disk = 0

        for l in self.get_stat(stat_name):
            if l[2] in self.block_devices and len(l) >= 14:
                # total io stat
                self.curr_stat['io'] = tuple(self.curr_stat['io'][i] + int(l[i + 3]) for i in range(11))
                num_disk += 1

                # per disk io stat
                self.curr_stat['io_' + l[2]] = tuple(int(l[i + 3]) for i in range(11))

            # https://www.percona.com/doc/percona-toolkit/2.1/pt-diskstats.html
        for disk in ['io'] + ['io_' + d for d in self.block_devices]:
            if disk not in self.curr_stat or disk not in self.old_stat:
                continue

            rd, rd_mrg, rd_sec, rd_tim, wr, wr_mrg, wr_sec, wr_tim, in_prg, t1, t2 = tuple(
                1.0 * (self.curr_stat[disk][i] - self.old_stat[disk][i])
                for i in range(11))
            in_prg = self.curr_stat[disk][8]

            rd_rt, wr_rt, busy, io_s, qtime, ttime, stime = tuple(0 for i in range(7))

            if rd + rd_mrg > 0:
                rd_rt = rd_tim / (rd + rd_mrg)
            if wr + wr_mrg > 0:
                wr_rt = wr_tim / (wr + wr_mrg)
            busy = 100 * t1 / 1000 / elapsed
            io_s = (rd + wr) / elapsed
            if rd + rd_mrg + wr + wr_mrg > 0:
                stime = t1 / (rd + rd_mrg + wr + wr_mrg)
            if rd + rd_mrg + wr + wr_mrg + in_prg > 0:
                ttime = t2 / (rd + rd_mrg + wr + wr_mrg + in_prg)

            qtime = ttime - stime

            rd_s, rd_avgkb, rd_m_s, rd_cnc, rd_mrg_s, wr_s, wr_avgkb, wr_m_s, wr_cnc, wr_mrg_s = tuple(
                0 for i in range(10))

            rd_s = rd / elapsed
            if rd > 0:
                rd_avgkb = rd_sec / rd / 2
            rd_m_s = rd_sec / 2 / 1024 / elapsed
            rd_cnc = rd_tim / 1000 / elapsed
            rd_mrg_s = rd_mrg / elapsed

            wr_s = wr / elapsed
            if wr > 0:
                wr_avgkb = wr_sec / wr / 2
            wr_m_s = wr_sec / 2 / 1024 / elapsed
            wr_cnc = wr_tim / 1000 / elapsed
            wr_mrg_s = wr_mrg / elapsed

            # io_read, io_write, io_queue, io_await, io_svctm, io_util, io_read_mb, io_write_mb,
            if disk == 'io':
                # total disk io stat
                self.stat[disk] = (rd_s, wr_s, in_prg, ttime, stime, busy / num_disk, rd_m_s, wr_m_s)
            else:
                label = ('rd_s', 'rd_avgkb', 'rd_m_s', 'rd_mrg_s', 'rd_cnc', 'rd_rt',
                         'wr_s','wr_avgkb','wr_m_s','wr_mrg_s','wr_cnc','wr_rt',
                         'busy', 'in_prg','io_s','qtime', 'stime')

                # per disk io stat
                self.stat[disk] = (rd_s, rd_avgkb, rd_m_s, rd_mrg_s, rd_cnc, rd_rt,
                              wr_s, wr_avgkb, wr_m_s, wr_mrg_s, wr_cnc, wr_rt,
                              busy, in_prg, io_s, qtime, stime)

                diskstat = format_stat(label, self.stat[disk])
                diskstat['dev'] = disk[3:]
                ret.append(diskstat)
            self.old_stat[disk] = self.curr_stat[disk]
        return ret


    def get_stat(self, stat_name, replace=None):
        stat_file = stat_file_config[stat_name]
        command = 'cat ' + stat_file
        res = super().exec_command(command,self.conn)
        fd = res

        for l in fd.readlines():
            if replace is not None:
                yield l.replace(replace, ' ').split()
            else:
                yield l.split()

    def get_diskfree(self):
        ret = []
        command = 'df -kP'
        res = super().exec_command(command,self.conn)
        disk_list = [line.split() for line in res]
        disk_list.pop(0)
        # print(disk_list)
        for each in disk_list:
            if each[0] == 'Filesystem' or each[0] == 'none' or each[0] == 'udev' or each[0] in "tmpfs"  or 'docker' in each[5] or each[5].startswith('/run') or 'cdrom' in each[5]:
                continue
            else:
                ret.append(each)
        # print(ret)
        return ret


if __name__ == '__main__':

    linux_params = {
        'hostname': '192.168.48.51',
        'port': 22,
        'username': 'root',
        'password': 'oracle'
    }
    linux_conn, _ = LinuxBase(linux_params).connection()

    linuxstat = LinuxStat(linux_params,linux_conn)

    print(linuxstat.get_host_info())


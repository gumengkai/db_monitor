# encoding:utf-8

import check.checklog as checklog
from utils.tools import mysql_exec,now,clear_table,archive_table
from check.linux_stat import LinuxStat
from utils.linux_base import LinuxBase
import timeout_decorator

@timeout_decorator.timeout(60)
def check_linux(tags,linux_params):
    check_time = now()
    host = linux_params['hostname']
    port = linux_params['port']
    # create connection
    linux_conn, _ = LinuxBase(linux_params).connection()
    try:
        checklog.logger.info('{}:开始获取Linux主机监控信息' .format(tags))
        # get linuxstat data
        linuxstat = LinuxStat(linux_params, linux_conn).get_linux()
        hostinfo = linuxstat['hostinfo']
        cpuinfo = linuxstat['cpuinfo']
        memtotal = linuxstat['Memtotal']
        ipinfo = linuxstat['ipinfo']
        load = linuxstat['load']
        cpustat = linuxstat['cpu']
        iostat = linuxstat['iostat']
        memstat = linuxstat['mem']
        vmstat = linuxstat['vmstat']
        tcpstat = linuxstat['tcpstat']
        netstat = linuxstat['net']
        procstat = linuxstat['proc']

        # total network in/out
        recv_kbps = round(sum([d['recv'] for d in netstat]),2)
        send_kbps = round(sum([d['send'] for d in netstat]),2)
        # total io
        read_mb = round(sum([d['rd_m_s'] for d in iostat]),2)
        write_mb = round(sum([d['wr_m_s'] for d in iostat]),2)
        iops = round(sum([d['io_s'] for d in iostat]),2)
        # cpu used percent
        cpu_used = round(100 - cpustat['cpu_idle'], 2)
        # memory used percent
        mem_used = round((float(memstat['mem_used_mb']) / (float(memtotal['memtotal']) / 1024)) * 100, 2)

        insert_data_values = {**locals(), **hostinfo, **cpuinfo, **memtotal, **ipinfo, **load, **cpustat, **memstat,
                              **vmstat, **tcpstat, **procstat}

        insert_data_sql = "insert into linux_stat(tags,host,port,hostname,ipinfo,linux_version,updays,kernel,frame,cpu_mode,cpu_cache,processor,cpu_speed," \
                          "recv_kbps,send_kbps,load1,load5,load15,cpu_sys,cpu_iowait,cpu_user,cpu_used,memtotal,mem_used,mem_cache,mem_buffer,mem_free,mem_used_mb," \
                          "swap_used,swap_free,swapin,swapout,pgin,pgout,pgfault,pgmjfault,tcp_close,tcp_timewait,tcp_connected,tcp_syn,tcp_listen,iops,read_mb,write_mb," \
                          "proc_new,proc_running,proc_block,intr,ctx,softirq,status,check_time) " \
                          "values ('{tags}','{host}',{port},'{hostname}','{ipinfo}','{linux_version}',{updays},'{kernel}','{frame}','{cpu_mode}','{cpu_cache}','{processor}','{cpu_speed}'," \
                          "{recv_kbps},{send_kbps},{load1},{load5},{load15},{cpu_sys},{cpu_iowait},{cpu_user},{cpu_used},{memtotal},{mem_used},{mem_cache},{mem_buffer},{mem_free},{mem_used_mb}," \
                          "{swap_used},{swap_free},{swapin},{swapout},{pgin},{pgout},{pgfault},{pgmjfault},{tcp_close},{tcp_timewait},{tcp_connected},{tcp_syn},{tcp_listen},{iops},{read_mb},{write_mb}," \
                          "{proc_new},{proc_running},{proc_block},{intr},{ctx},{softirq},0,'{check_time}')"

        clear_table(tags,'linux_stat')
        insert_sql = insert_data_sql.format(**insert_data_values)
        mysql_exec(insert_sql)
        archive_table(tags,'linux_stat')

        # disk free
        clear_table(tags,'linux_disk')
        diskfree_list = LinuxStat(linux_params, linux_conn).get_diskfree()
        for each in diskfree_list:
            dev, total_size, used_size, free_size, used_percent, mount_point = each
            used_percent = float(used_percent.replace('%',''))
            insert_data_sql = '''insert into linux_disk(tags,host,dev,total_size,used_size,free_size,used_percent,mount_point,check_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            values = (tags, host, dev, round(float(total_size)/1024/1024, 2), round(float(used_size)/1024/1024, 2),
                      round(float(free_size)/1024/1024, 2), used_percent, mount_point, now())
            mysql_exec(insert_data_sql, values)
        archive_table(tags,'linux_disk')

        # io stat
        clear_table(tags,'linux_io_stat')
        for each in iostat:
            insert_data_sql = "insert into linux_io_stat(tags,host,dev,rd_s,rd_avgkb,rd_m_s,rd_mrg_s,rd_cnc,rd_rt,wr_s,wr_avgkb,wr_m_s,wr_mrg_s,wr_cnc,wr_rt,busy,in_prg,io_s,qtime,stime,check_time)" \
                              " values ('{tags}','{host}','{dev}',{rd_s},{rd_avgkb},{rd_m_s},{rd_mrg_s},{rd_cnc},{rd_rt},{wr_s},{wr_avgkb},{wr_m_s},{wr_mrg_s},{wr_cnc},{wr_rt},{busy},{in_prg},{io_s},{qtime},{stime},'{check_time}')"
            insert_data_values = {**locals(), **each}
            insert_sql = insert_data_sql.format(**insert_data_values)
            mysql_exec(insert_sql)
        archive_table(tags,'linux_io_stat')
    except Exception as e:
        error_msg = "{}:linux主机连接失败,{}" .format(tags,e)
        checklog.logger.error(error_msg)
        checklog.logger.info('{}:写入linux_stat采集数据'.format(tags))
        clear_table(tags,'linux_stat')
        sql = "insert into linux_stat(tags,host,port,status,check_time) values('{tags}','{host}',{port},1,'{check_time}')"
        sql = sql.format(**locals())
        mysql_exec(sql)
        archive_table(tags,'linux_stat')

if __name__ == '__main__':
    print(now())

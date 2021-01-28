from celery import shared_task
from check.maincheck import checkall
from utils.oracle_rac_install import OracleRacInstall

@shared_task
def main_check():
    checkall()
    return

# oracle性能报告
@shared_task
def oracle_rac_setup(rac_info,node_list,module):
    print('Oracle RAC安装已启动！')
    oracleracinstall = OracleRacInstall(rac_info, node_list)
    oracleracinstall.do_rac_install(module)

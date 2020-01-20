# encoding:utf-8

from utils.oracle_base import OracleBase
import json

if __name__ == '__main__':
    oracle_params = {
        'host': '192.168.48.60',
        'port': 1521,
        'service_name': 'pdb1',
        'user': 'dbmon',
        'password': 'oracle',
        'service_name_cdb': 'orcl19c',
        'user_cdb': 'c##dbmon',
        'password_cdb': 'oracle'
    }
    db_conn = OracleBase(oracle_params).connection()
    OracleBase(oracle_params).call_proc('pro_top_cpu_sql',db_conn)
    sql = "select ID,COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8,COL9,COL10,COL11,COL12," \
          "SHOW_TYPE,SHOW_TITLE,INST_INFO from snap_show_config"
    res_config = OracleBase(oracle_params).query_one(sql,db_conn)
    sql = "select ID,RATE,SQL_ID,SQL_EXEC_CNT,VAL1,VAL2,VAL3,VAL4,VAL4,VAL5,VAL6,VAL7,VAL8," \
          "VAL9,SNAP_TYPE_ID from snap_show"
    res_data = OracleBase(oracle_params).query_all(sql,db_conn)

    data = {
        'snap_config':res_config,
        'snap_data':res_data
    }
    print(json.dumps(data))





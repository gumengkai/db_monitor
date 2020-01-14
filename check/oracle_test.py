import cx_Oracle

from utils.oracle_base import OracleBase

params = {
    'host': '192.168.48.10',
    'port': 1521,
    'service_name': 'pdb1',
    'user': 'dbmon',
    'password': 'oracle',
    'service_name_cdb': 'orcl',
    'user_cdb': 'c##dbmon',
    'password_cdb': 'oracle',
    'db_version': 'Oracle12c'
}


if __name__ == '__main__':
    params = {
        'host': '192.168.48.10',
        'port': 1521,
        'service_name': 'pdb1',
        'user': 'dbmon',
        'password': 'oracle',
        'service_name_cdb': 'orcl',
        'user_cdb': 'c##dbmon',
        'password_cdb': 'oracle',
        'db_version': 'Oracle12c'
    }

    host = params['host']
    port = params['port']
    service_name = params['service_name']
    user = params['user']
    password = params['password']
    oracle_url = '{}:{}/{}'.format(host,port,service_name)
    conn = cx_Oracle.connect(user, password, oracle_url)


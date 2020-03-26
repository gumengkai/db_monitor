#! /usr/bin/python
# encoding:utf-8

# Create your tasks here

from __future__ import absolute_import,unicode_literals
from celery import shared_task
from utils.oracle_report import OracleReport
from utils.oracle_base import OracleBase

# oracle性能报告
@shared_task
def create_oracle_report(tags,oracle_params,report_type,begin_snap,end_snap):
    print('task begin!')
    # db_conn = OracleBase(oracle_params).connection()
    db_conn_cdb = OracleBase(oracle_params).connection_cdb()
    oracle_report = OracleReport(db_conn_cdb,tags,oracle_params)
    oracle_report.get_report(report_type,begin_snap,end_snap)

# encoding:utf-8

from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as dfilters
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from .serializers import *
import json
from utils.tools import *
from utils.django_tools import NoPagination
from utils.oracle_base import OracleBase

# not using
class OraclestatFilter(dfilters.FilterSet):
    start_time = dfilters.DateTimeFilter(field_name="check_time",lookup_expr='gte')
    end_time = dfilters.DateTimeFilter(field_name="check_time",lookup_expr='lte')
    class Meta:
        model = OracleStat
        fields = ['tags','host','start_time','end_time']

class ApiOracleStat(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        return OracleStat.objects.filter(status=0, tags=tags).order_by('-status')
    serializer_class = OracleStatSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiOracleStatHis(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        start_time = self.request.query_params.get('start_time',None)
        end_time = self.request.query_params.get('end_time',None)
        if start_time and end_time:
            start_time = get_utctime(start_time)
            end_time = get_utctime(end_time)
        else:
            # default data of 1 day
            end_time = today()
            start_time = last_day()
        return OracleStatHis.objects.filter(tags=tags, check_time__gte=start_time, check_time__lte=end_time).order_by('check_time')

    serializer_class = OracleStatHisSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

# all instance
class ApiOracleStatList(generics.ListCreateAPIView):
    queryset = OracleStat.objects.get_queryset().order_by('-id')
    serializer_class = OracleStatSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host','status')
    search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiOracleTableSpace(generics.ListCreateAPIView):
    queryset = OracleTableSpace.objects.get_queryset().order_by('-id')
    serializer_class = OracleTableSpaceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host')
    search_fields = ('tags', 'host')
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiOracleTableSpaceHis(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        tablespace_name = self.request.query_params.get('tablespace_name', None)
        start_time = self.request.query_params.get('start_time',None)
        end_time = self.request.query_params.get('end_time',None)
        if start_time and end_time:
            start_time = get_utctime(start_time)
            end_time = get_utctime(end_time)
        else:
            # default data of 1 day
            end_time = today()
            start_time = last_day()
        return OracleTableSpaceHis.objects.filter(tags=tags,tablespace_name=tablespace_name,check_time__gte=start_time, check_time__lte=end_time).order_by('check_time')

    serializer_class = OracleTableSpaceHisSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleTableSpaceLargeObject(request):
    tags = request.GET.get('tags')
    tablespace_name = request.GET.get('tablespace_name')
    oracle_params = get_oracle_params(tags)
    sql = "select owner, segment_name, round(sum(bytes) / 1024 / 1024 ,2) gbytes from " \
          "dba_segments where tablespace_name = '{}'  " \
          "group by owner, segment_name having sum(bytes) / 1024 / 1024 > 10".format(tablespace_name)
    largeobject_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleTableSpaceLargeObjectSerializer(largeobject_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleTableSpaceDayUsed(request):
    tags = request.GET.get('tags')
    tablespace_name = request.GET.get('tablespace_name')
    oracle_params = get_oracle_params(tags)
    sql = "select to_char(trunc(to_date(rtime, 'mm/dd/yyyy hh24:mi:ss'), 'dd'),'yyyy-mm-dd') m_date,b.name," \
          "round(sum(tablespace_usedsize) / 1024 / 1024) used_mb " \
          "from dba_hist_tbspc_space_usage a, v$tablespace b " \
          "where a.tablespace_id = b.ts# and b.name = '{}' " \
          "and to_date(rtime, 'mm/dd/yyyy hh24:mi:ss')>sysdate-6 " \
          "group by to_char(trunc(to_date(rtime, 'mm/dd/yyyy hh24:mi:ss'), 'dd'),'yyyy-mm-dd'),b.name".format(tablespace_name)
    dayused_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleTableSpaceDayUsedSerializer(dayused_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)


class ApiOracleTempTableSpace(generics.ListCreateAPIView):
    queryset = OracleTempTableSpace.objects.get_queryset().order_by('-id')
    serializer_class = OracleTempTableSpaceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host')
    search_fields = ('tags', 'host')
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiOracleTempTableSpaceHis(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        temptablespace_name = self.request.query_params.get('temptablespace_name', None)
        start_time = self.request.query_params.get('start_time',None)
        end_time = self.request.query_params.get('end_time',None)
        if start_time and end_time:
            start_time = get_utctime(start_time)
            end_time = get_utctime(end_time)
        else:
            # default data of 1 day
            end_time = today()
            start_time = last_day()
        return OracleTempTableSpaceHis.objects.filter(tags=tags,temptablespace_name=temptablespace_name,check_time__gte=start_time, check_time__lte=end_time).order_by('check_time')

    serializer_class = OracleTempTableSpaceHisSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleTempTableSpaceSessionUsed(request):
    tags = request.GET.get('tags')
    temptablespace_name = request.GET.get('temptablespace_name')
    oracle_params = get_oracle_params(tags)
    sql = "SELECT S.sid ,S.username, S.osuser, P.spid, S.module,S.program,SUM(T.blocks) * TBS.block_size / 1024/1024  mb_used," \
          "T.tablespace,COUNT(*) sort_ops FROM v$sort_usage T, v$session S, dba_tablespaces TBS, v$process P " \
          "WHERE T.session_addr = S.saddr AND S.paddr = P.addr AND T.tablespace = TBS.tablespace_name AND T.tablespace='{}' " \
          "GROUP BY S.sid,S.serial#,S.username,S.osuser,P.spid,S.module,S.program,TBS.block_size,T.tablespace".format(temptablespace_name)
    sessionused_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleTempTableSpaceSessionUsedSerializer(sessionused_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)


class ApiOracleUndoTableSpace(generics.ListCreateAPIView):
    queryset = OracleUndoTableSpace.objects.get_queryset().order_by('-percent_used')
    serializer_class = OracleUndoTableSpaceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'host')
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiOracleUndoTableSpaceHis(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        undotablespace_name = self.request.query_params.get('undotablespace_name', None)
        start_time = self.request.query_params.get('start_time',None)
        end_time = self.request.query_params.get('end_time',None)
        if start_time and end_time:
            start_time = get_utctime(start_time)
            end_time = get_utctime(end_time)
        else:
            # default data of 1 day
            end_time = today()
            start_time = last_day()
        return OracleUndoTableSpaceHis.objects.filter(tags=tags,undotablespace_name=undotablespace_name,check_time__gte=start_time, check_time__lte=end_time).order_by('check_time')

    serializer_class = OracleUndoTableSpaceHisSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleUndoTableSpaceSessionUsed(request):
    tags = request.GET.get('tags')
    undotablespace_name = request.GET.get('undotablespace_name')
    oracle_params = get_oracle_params(tags)
    sql = "SELECT r.name rbs,nvl(s.username, 'None') oracle_user,s.osuser client_user,p.username unix_user,s.program,s.sid," \
          "s.serial#,p.spid unix_pid,t.used_ublk * TO_NUMBER(x.value) / 1024 / 1024 as undo_mb," \
          "TO_CHAR(s.logon_time, 'mm/dd/yy hh24:mi:ss') as login_time,TO_CHAR(sysdate - (s.last_call_et) / 86400, 'mm/dd/yy hh24:mi:ss') as last_txn," \
          "t.START_TIME transaction_starttime " \
          "FROM v$process p,v$rollname r,v$session s,v$transaction t,v$parameter x" \
          " WHERE s.taddr = t.addr AND s.paddr = p.addr AND r.usn = t.xidusn(+) AND x.name = 'db_block_size' ".format(undotablespace_name)
    sessionused_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleUndoTableSpaceSessionUsedSerializer(sessionused_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleUndoTableSpaceUsed(request):
    tags = request.GET.get('tags')
    undotablespace_name = request.GET.get('undotablespace_name')
    oracle_params = get_oracle_params(tags)
    sql = "select tablespace_name, status, sum(bytes) / 1024 / 1024 MB from dba_undo_extents " \
          "where tablespace_name = '{}' group by tablespace_name, status".format(undotablespace_name)
    undoused_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleUndoTableSpaceUsedSerializer(undoused_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

class ApiOracleTableStats(generics.ListAPIView):
    queryset = OracleTableStats.objects.get_queryset().order_by('-change_pct')
    serializer_class = OracleTableStatsSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiOracleControlFile(generics.ListAPIView):
    queryset = OracleControlFile.objects.get_queryset().order_by('name')
    serializer_class = OracleControlFileSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class ApiOracleRedoLog(generics.ListAPIView):
    queryset = OracleRedoLog.objects.get_queryset().order_by('group_no')
    serializer_class = OracleRedoLogSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleRedoLogSwitch(request):
    tags = request.GET.get('tags')
    redo_range = request.GET.get('redo_range')
    oracle_params = get_oracle_params(tags)
    if int(redo_range) == 1:
        sql = '''
        select  'hh'||to_char(first_time, 'hh24') stat_date,
                count(1) log_count,
                (select bytes / 1024 / 1024 sizem from v$log where rownum < 2) log_size
           from v$log_history
          where to_char(first_time, 'yyyymmdd') < to_char(sysdate, 'yyyymmdd')
            and to_char(first_time, 'yyyymmdd') >=
                to_char(sysdate - 1, 'yyyymmdd')
          group by to_char(first_time, 'hh24'),to_char(first_time, 'dy')
          order by to_char(first_time, 'hh24')'''
    else:
        sql = '''
        select to_char(first_time, 'yyyy-mm-dd') stat_date,
               count(1) log_count,
              (select bytes / 1024 / 1024 sizem from v$log where rownum < 2) log_size
          from v$log_history
        where to_char(first_time, 'yyyymmdd') < to_char(sysdate, 'yyyymmdd')
          and to_char(first_time, 'yyyymmdd') >= to_char(sysdate - {}, 'yyyymmdd')
        group by to_char(first_time, 'yyyy-mm-dd'), to_char(first_time, 'dy')
        order by to_char(first_time, 'yyyy-mm-dd')
        '''.format(redo_range)
    redoswitch_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleRedoSwitchSerializer(redoswitch_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleTopSegment(request):
    tags = request.GET.get('tags')
    oracle_params = get_oracle_params(tags)
    sql = '''
    select *
  from (select a.owner,
               a.segment_name,
               a.partition_name,
               a.segment_type,
               a.tablespace_name,
               a.bytes / 1024 / 1024  segment_size,
               row_number() over(order by a.bytes desc) RN
          from dba_segments a)
 where rn <= 50
    '''
    top_segment_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleTopSegmentSerializer(top_segment_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleSequenceUsed(request):
    tags = request.GET.get('tags')
    oracle_params = get_oracle_params(tags)
    sql = '''select sequence_owner,sequence_name,min_value,max_value,increment_by,cycle_flag,order_flag,
       cache_size,last_number,
       round((max_value - last_number) / (max_value - min_value), 2) * 100 pct_used
  from dba_sequences s
 where s.sequence_owner not in ('SYS','SYSTEM','OUTLN','DIP','ORACLE_OCM','DBSNMP','APPQOSSYS','WMSYS','EXFSYS',
'CTXSYS','ANONYMOUS','XDB','XS$NULL','ORDDATA','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','MDSYS','OLAPSYS',
'MDDATA','SPATIAL_WFS_ADMIN_USR','SPATIAL_CSW_ADMIN_USR','SYSMAN','MGMT_VIEW','APEX_030200','FLOWS_FILES',
'APEX_PUBLIC_USER','OWBSYS','OWBSYS_AUDIT','SCOTT') '''
    sequence_used_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleSequenceUsedSerializer(sequence_used_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleUser(request):
    tags = request.GET.get('tags')
    oracle_params = get_oracle_params(tags)
    sql = '''select username,profile,to_char(created,'yyyy-mm-dd hh24:mi:ss') created,
                   account_status,
                   to_char(lock_date,'yyyy-mm-dd hh24:mi:ss') lock_date,
                   to_char(expiry_date,'yyyy-mm-dd hh24:mi:ss') expiry_date,
                   default_tablespace,temporary_tablespace
            from dba_users order by created desc '''
    user_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleUserSerializer(user_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleProfile(request):
    tags = request.GET.get('tags')
    profile = request.GET.get('profile')
    oracle_params = get_oracle_params(tags)
    sql = """
                select profile,resource_name,resource_type,limit
                  from dba_profiles where  profile = '{}'
                """.format(profile)
    profile_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleProfileSerializer(profile_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleUserRole(request):
    tags = request.GET.get('tags')
    user = request.GET.get('user')
    oracle_params = get_oracle_params(tags)
    sql = "select grantee,granted_role, admin_option,default_role from dba_role_privs where grantee = '{}' ".format(user)
    role_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleUserRoleSerializer(role_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleUserGrant(request):
    tags = request.GET.get('tags')
    user = request.GET.get('user')
    oracle_params = get_oracle_params(tags)
    sql = "select grantee,privilege,admin_option from dba_sys_privs where grantee = '{}' ".format(user)
    grant_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleUserGrantSerializer(grant_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleActiveSession(request):
    tags = request.GET.get('tags')
    oracle_params = get_oracle_params(tags)
    sql = '''
    select to_char(a.logon_time, 'yyyy-mm-dd hh24:mi') logon_time,
       a.sql_id,
       a.event,
       a.blocking_session,
       a.username,
       a.osuser,
       a.process,
       a.machine,
       a.program,
       a.module,
       b.sql_text,
       b.LAST_LOAD_TIME,
       to_char(b.last_active_time, 'yyyy-mm-dd hh24:mi:ss') last_active_time,
       c.owner,
       c.object_name,
       a.last_call_et,
       a.sid,
       a.SQL_CHILD_NUMBER,
       c.object_type,
       p.PGA_ALLOC_MEM,
       a.p1,
       a.p2,
       a.p3,
       'kill -9 ' || p.spid killstr,
  'ps -ef|grep '|| p.spid ||'|grep LOCAL=NO|awk ''{print $2}''|xargs kill -9' kill_sh
    from v$session a, v$sql b, dba_objects c, v$process p
   where a.status = 'ACTIVE'
   and p.addr = a.paddr
   and a.sql_id = b.sql_id(+)
  -- and a.wait_class <> 'Idle'
   and a.sql_child_number = b.CHILD_NUMBER(+)
   and a.row_wait_obj# = c.object_id(+)
   and a.type = 'USER' '''
    active_session_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleActiveSession(active_session_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleBlockingSession(request):
    tags = request.GET.get('tags')
    oracle_params = get_oracle_params(tags)
    sql = '''
    select to_char(a.logon_time, 'yyyy-mm-dd hh24:mi') logon_time,
       a.sid,
       a.sql_id,
       a.event,
       a.blocking_session,
       a.username,
       a.osuser,
       a.machine,
       a.program,
       a.module,
       b.sql_text,
       c.owner,
       c.object_name,
       c.object_type
  from v$session a, v$sql b, dba_objects c, v$process p
 where a.state in ('WAITING')
   and a.wait_class != 'Idle'
   and p.addr = a.paddr
   and a.sql_id = b.sql_id(+)
   and a.sql_child_number = b.CHILD_NUMBER(+)
   and a.row_wait_obj# = c.object_id(+)
    '''
    blocking_session_list = OracleBase(oracle_params).django_query(sql)
    serializer = OracleBlockingSession(blocking_session_list,many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleSessionCount(request):
    tags = request.GET.get('tags')
    oracle_params = get_oracle_params(tags)
    sql = '''
    select a.status,count(*) cnt from v$session a where a.type='USER' group by a.status
    '''
    session_all = OracleBase(oracle_params).django_query(sql)
    active_session_count = 0
    inactive_session_count = 0
    for each in session_all:
        if each['STATUS'] == 'ACTIVE':
            active_session_count = each['CNT']
        if each['STATUS'] == 'INACTIVE':
            inactive_session_count = each['CNT']
    session_count_data = {'ACTIVE':active_session_count,'INACTIVE':inactive_session_count}
    return HttpResponse(json.dumps(session_count_data))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleBlockCount(request):
    tags = request.GET.get('tags')
    oracle_params = get_oracle_params(tags)
    sql = '''
    select event, count(1) cnt
    from v$session
    where wait_class != 'Idle'
    group by event
    '''
    block_all = OracleBase(oracle_params).django_query(sql)
    row_lock_count = sum([each['CNT'] for each in block_all if each['EVENT']=='enq: TX - row lock contention'])
    all_block_count = sum([each['CNT'] for each in block_all])

    block_count_data = {'ROW_LOCK':row_lock_count,'ALL':all_block_count}
    return HttpResponse(json.dumps(block_count_data))


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApiOracleTopSql(request):
    tags = request.GET.get('tags')
    type = request.GET.get('type')
    oracle_params = get_oracle_params(tags)
    dic_proc = {
        'cpu':'pro_top_cpu_sql',
        'phys':'pro_top_phys_sql',
        'logic':'pro_top_logic_sql'
    }
    proc_name = dic_proc.get(type)
    db_conn = OracleBase(oracle_params).connection()
    OracleBase(oracle_params).call_proc(proc_name, db_conn)
    sql = "select COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8,COL9,COL10,COL11,COL12 from snap_show_config " \
          "union all " \
          "select RATE,SQL_ID,SQL_EXEC_CNT,VAL1,VAL2,VAL3,VAL4,VAL5,VAL6,VAL7,VAL8,VAL9 from snap_show"
    res = OracleBase(oracle_params).django_query(sql, db_conn)
    serializer = OracleTopSql(res, many=True)
    snap_json = JSONRenderer().render(serializer.data)
    return HttpResponse(snap_json)

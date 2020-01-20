from rest_framework import serializers
from .models import *

class OracleStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleStat
        fields = '__all__'

class OracleStatHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleStatHis
        fields = '__all__'

class OracleTableSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleTableSpace
        fields = '__all__'

class OracleTableSpaceHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleTableSpaceHis
        fields = '__all__'

class OracleTableSpaceLargeObjectSerializer(serializers.Serializer):
    OWNER = serializers.CharField()
    SEGMENT_NAME = serializers.CharField()
    GBYTES = serializers.FloatField()

class OracleTableSpaceDayUsedSerializer(serializers.Serializer):
    M_DATE = serializers.CharField()
    NAME = serializers.CharField()
    USED_MB = serializers.FloatField()

class OracleTempTableSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleTempTableSpace
        fields = '__all__'

class OracleTempTableSpaceHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleTempTableSpaceHis
        fields = '__all__'

class OracleTempTableSpaceSessionUsedSerializer(serializers.Serializer):
    SID = serializers.IntegerField()
    USERNAME = serializers.CharField()
    OSUSER = serializers.CharField()
    SPID = serializers.IntegerField()
    MODULE = serializers.CharField()
    PROGRAM = serializers.CharField()
    MB_USED = serializers.FloatField()
    TABLESPACE = serializers.CharField()
    SORT_OPS = serializers.IntegerField()

class OracleUndoTableSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleUndoTableSpace
        fields = '__all__'

class OracleUndoTableSpaceHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleUndoTableSpaceHis
        fields = '__all__'

class OracleUndoTableSpaceUsedSerializer(serializers.Serializer):
    TABLESPACE_NAME = serializers.CharField()
    STATUS = serializers.CharField()
    MB = serializers.FloatField()

class OracleUndoTableSpaceSessionUsedSerializer(serializers.Serializer):
    SID = serializers.IntegerField()
    RBS = serializers.CharField()
    ORACLE_USER = serializers.CharField()
    CLIENT_USER = serializers.CharField()
    UNIX_USER = serializers.CharField()
    PROGRAM = serializers.CharField()
    UNIX_PID = serializers.IntegerField()
    UNDO_MB = serializers.FloatField()
    LOGIN_TIME = serializers.CharField()
    LAST_TXN = serializers.CharField()
    TRANSACTION_STARTTIME = serializers.CharField()

class OracleTableStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleTableStats
        fields = '__all__'

class OracleControlFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleControlFile
        fields = '__all__'

class OracleRedoLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OracleRedoLog
        fields = '__all__'

class OracleRedoSwitchSerializer(serializers.Serializer):
    STAT_DATE = serializers.CharField()
    LOG_COUNT = serializers.IntegerField()

class OracleTopSegmentSerializer(serializers.Serializer):
    OWNER = serializers.CharField()
    SEGMENT_NAME = serializers.CharField()
    PARTITION_NAME = serializers.CharField()
    SEGMENT_TYPE = serializers.CharField()
    TABLESPACE_NAME = serializers.CharField()
    SEGMENT_SIZE = serializers.FloatField()
    RN = serializers.IntegerField()

class OracleSequenceUsedSerializer(serializers.Serializer):
    SEQUENCE_OWNER = serializers.CharField()
    SEQUENCE_NAME = serializers.CharField()
    MIN_VALUE = serializers.IntegerField()
    MAX_VALUE = serializers.CharField()
    INCREMENT_BY = serializers.IntegerField()
    CYCLE_FLAG = serializers.CharField()
    ORDER_FLAG = serializers.CharField()
    CACHE_SIZE = serializers.IntegerField()
    LAST_NUMBER = serializers.IntegerField()

class OracleUserSerializer(serializers.Serializer):
    USERNAME = serializers.CharField()
    PROFILE = serializers.CharField()
    CREATED = serializers.CharField()
    ACCOUNT_STATUS = serializers.CharField()
    LOCK_DATE = serializers.CharField()
    EXPIRY_DATE = serializers.CharField()
    DEFAULT_TABLESPACE = serializers.CharField()
    TEMPORARY_TABLESPACE = serializers.CharField()

class OracleProfileSerializer(serializers.Serializer):
    PROFILE = serializers.CharField()
    RESOURCE_NAME = serializers.CharField()
    RESOURCE_TYPE = serializers.CharField()
    LIMIT = serializers.CharField()

class OracleUserRoleSerializer(serializers.Serializer):
    GRANTEE = serializers.CharField()
    GRANTED_ROLE = serializers.CharField()
    ADMIN_OPTION = serializers.CharField()

class OracleUserGrantSerializer(serializers.Serializer):
    GRANTEE = serializers.CharField()
    PRIVILEGE = serializers.CharField()
    ADMIN_OPTION = serializers.CharField()

class OracleActiveSession(serializers.Serializer):
    LOGON_TIME = serializers.CharField()
    SID = serializers.IntegerField()
    SQL_ID = serializers.CharField()
    EVENT = serializers.CharField()
    BLOCKING_SESSION = serializers.IntegerField()
    USERNAME = serializers.CharField()
    OSUSER = serializers.CharField()
    PROCESS = serializers.CharField()
    MACHINE = serializers.CharField()
    PROGRAM = serializers.CharField()
    MODULE = serializers.CharField()
    SQL_TEXT = serializers.CharField()
    LAST_LOAD_TIME = serializers.CharField()
    LAST_ACTIVE_TIME = serializers.CharField()
    OWNER = serializers.CharField()
    OBJECT_NAME = serializers.CharField()
    LAST_CALL_ET = serializers.IntegerField()
    SQL_CHILD_NUMBER = serializers.IntegerField()
    OBJECT_TYPE = serializers.CharField()
    PGA_ALLOC_MEM = serializers.IntegerField()
    P1 = serializers.IntegerField()
    P2 = serializers.IntegerField()
    P3 = serializers.IntegerField()
    KILLSTR = serializers.CharField()
    KILL_SH = serializers.CharField()

class OracleBlockingSession(serializers.Serializer):
    LOGON_TIME = serializers.CharField()
    SID = serializers.IntegerField()
    SQL_ID = serializers.CharField()
    EVENT = serializers.CharField()
    BLOCKING_SESSION = serializers.IntegerField()
    USERNAME = serializers.CharField()
    OSUSER = serializers.CharField()
    MACHINE = serializers.CharField()
    PROGRAM = serializers.CharField()
    MODULE = serializers.CharField()
    SQL_TEXT = serializers.CharField()
    OWNER = serializers.CharField()
    OBJECT_NAME = serializers.CharField()
    OBJECT_TYPE = serializers.CharField()

class OracleTopSql(serializers.Serializer):
    COL1 = serializers.CharField()
    COL2 = serializers.CharField()
    COL3 = serializers.CharField()
    COL4 = serializers.CharField()
    COL5 = serializers.CharField()
    COL6 = serializers.CharField()
    COL7 = serializers.CharField()
    COL8 = serializers.CharField()
    COL9 = serializers.CharField()
    COL10 = serializers.CharField()
    COL11 = serializers.CharField()
    COL12 = serializers.CharField()

from django.urls import path
from oracle import views

app_name = "oracle"

urlpatterns = [
    path('api/oracle-stat-list', views.ApiOracleStatList.as_view()),
    path('api/oracle-stat', views.ApiOracleStat.as_view()),
    path('api/oracle-stat-his', views.ApiOracleStatHis.as_view()),
    path('api/oracle-tablespace', views.ApiOracleTableSpace.as_view()),
    path('api/oracle-tablespace-his', views.ApiOracleTableSpaceHis.as_view()),
    path('api/oracle-tablespace-largeobject', views.ApiOracleTableSpaceLargeObject),
    path('api/oracle-tablespace-dayused', views.ApiOracleTableSpaceDayUsed),
    path('api/oracle-temp-tablespace', views.ApiOracleTempTableSpace.as_view()),
    path('api/oracle-temptablespace-his', views.ApiOracleTempTableSpaceHis.as_view()),
    path('api/oracle-temptablespace-sessionused', views.ApiOracleTempTableSpaceSessionUsed),
    path('api/oracle-undo-tablespace', views.ApiOracleUndoTableSpace.as_view()),
    path('api/oracle-undotablespace-his', views.ApiOracleUndoTableSpaceHis.as_view()),
    path('api/oracle-undotablespace-sessionused', views.ApiOracleUndoTableSpaceSessionUsed),
    path('api/oracle-undotablespace-used', views.ApiOracleUndoTableSpaceUsed),
    path('api/oracle-top-segment', views.ApiOracleTopSegment),
    path('api/oracle-sequence-used', views.ApiOracleSequenceUsed),
    path('api/oracle-user', views.ApiOracleUser),
    path('api/oracle-profile', views.ApiOracleProfile),
    path('api/oracle-user-role', views.ApiOracleUserRole),
    path('api/oracle-user-grant', views.ApiOracleUserGrant),
    path('api/oracle-active-session', views.ApiOracleActiveSession),
    path('api/oracle-blocking-session', views.ApiOracleBlockingSession),
    path('api/oracle-session-count', views.ApiOracleSessionCount),
    path('api/oracle-block-count', views.ApiOracleBlockCount),
    path('api/oracle-table-stats', views.ApiOracleTableStats.as_view()),
    path('api/oracle-controlfile', views.ApiOracleControlFile.as_view()),
    path('api/oracle-redolog', views.ApiOracleRedoLog.as_view()),
    path('api/oracle-redolog-switch', views.ApiOracleRedoLogSwitch),
    path('api/oracle-top-sql', views.ApiOracleTopSql),
]


from django.urls import path
from system.views import UserInfo,UserLogout,Menu
from system import views

app_name = "system"

urlpatterns = [
    path('api/user_info', UserInfo.as_view()),
    path('api/logout', UserLogout.as_view()),
    path('menu', Menu.as_view()),
    path('api/alert-log', views.ApiAlertLog.as_view()),
    path('api/alarm-conf', views.ApiAlarmConf.as_view()),
    path('api/alarm-conf/<int:pk>', views.ApiAlarmConfDetail.as_view()),
    path('api/alarm-info', views.ApiAlarmInfo.as_view()),
    path('api/oracle-rac-setup', views.ApiOracleRacSetup),
    path('api/oracle-rac-onenode-setup', views.ApiOracleRacOneNodeSetup),
    path('api/oracle-onenode-setup', views.ApiOracleOneNodeSetup),
    path('api/mysql-setup', views.ApiMysqlSetup),
    path('api/setup-log', views.ApiSetupLog),
]

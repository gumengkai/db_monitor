from django.urls import path
from assets import views

app_name = "assets"

urlpatterns = [
    path('api/oracle', views.ApiOracleList.as_view()),
    path('api/oracle/<int:pk>', views.ApiOracleDetail.as_view()),
    path('api/mysql', views.ApiMysqlList.as_view()),
    path('api/mysql/<int:pk>', views.ApiMysqlDetail.as_view()),
    path('api/linux', views.ApiLinuxList.as_view()),
    path('api/linux/<int:pk>', views.ApiLinuxDetail.as_view()),
    path('api/redis', views.ApiRedisList.as_view()),
    path('api/redis/<int:pk>', views.ApiRedisDetail.as_view()),
]


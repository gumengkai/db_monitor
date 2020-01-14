from django.urls import path
from rds import views

app_name = "rds"

urlpatterns = [
    path('api/redis-stat-list', views.ApiRedisStatList.as_view()),
    path('api/redis-stat', views.ApiRedisStat.as_view()),
    path('api/redis-stat-his', views.ApiRedisStatHis.as_view()),
    path('api/get-redis-config', views.ApiRedisConfig),
    path('api/get-redis-slowlog', views.ApiRedisSlowLog),
    path('api/get-redis-clientlist', views.ApiRedisClientList),
    path('api/get-redis-immediate-stats', views.ApiRedisImmediateStats),
]

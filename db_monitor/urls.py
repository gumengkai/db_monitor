"""db_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth',views.obtain_auth_token),
    path('system/',include('system.urls',namespace='system')),
    path('assets/', include('assets.urls',namespace='assets')),
    path('oracle/', include('oracle.urls', namespace='oracle')),
    path('mysql/', include('mysql.urls', namespace='mysql')),
    path('rds/', include('rds.urls', namespace='rds')),
    path('linux/', include('linux.urls', namespace='linux')),
]

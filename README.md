
# DB monitor数据库监控平台

![](https://img.shields.io/badge/build-release-brightgreen.svg)
![](https://img.shields.io/badge/version-v1.0.0-brightgreen.svg)
![](https://img.shields.io/badge/vue.js-2.9.6-brightgreen.svg)
![](https://img.shields.io/badge/iview-3.4.0-brightgreen.svg?style=flat-square)
![](https://img.shields.io/badge/python-3.6-brightgreen.svg)
![](https://img.shields.io/badge/Django-2.2-brightgreen.svg)

## 特性
- **构建**: 前后端分离架构，Python+Django+restframework提供后台API，celery定制数据采集策略，Iview作为前端展示
- **UI**: 开箱即用的高质量前端设计，提供丰富的图表、指标展示，核心数据形成趋势图分析
- **深度定制**: 提供完整可用的数据监控方案，告别冗长的SQL脚本、常用手册，复杂数据通过web页面即可轻易浏览

## 功能简介

- 资源管理
    - Oracle/MySQL/Redis/Linux资源信息录入
    - 资源管理中各类设备信息作为采集设备来源，支持动态加入实例监控列表
- 实例列表
    - 查看各监控实例列表及详细信息
- 监控告警
    - 告警配置及告警信息查看
- 数据库部署
    - 支持Oracle19c RAC/RAC One Node/单实例，MySQL5.7/8.0单实例部署
    
## 环境

- Python 3.6
    - Django 2.2
    - Django Rest Framework 3.1
    
- Vue.js 2.9
    - iview 3.4

## 平台使用
- [在线访问](http://122.51.204.250:8080/) (推荐使用chrome浏览器)
  
用户名：admin 
密码：111111

注：资源紧张及各种原因，demo已停用，想看的同学可以自行部署。

懒人以及没有接触过的建议使用docker部署方式

docker部署可参考：
https://blog.csdn.net/gumengkai/article/details/106250548

docker(懒人详细版)部署可参考，提供所有安装文件，可以直接在内网使用：
https://stuxidianeducn-my.sharepoint.com/:f:/g/personal/gumengkai_stu_xidian_edu_cn/EljbazMtQtJKhPKsuY9ZljgBjp7ujQHxPfj6-Hk0dnhyxQ?e=8JOrTk

## 安装部署
### 1. 安装python3.6(略)

### 2. 安装mysql5.7(略)

注意字符集：utf-8

create database db_monitor; 

### 3. 安装redis3.2(略)

### 4. 安装oracle instant client(略)

### 5. 项目配置

#### 下载源代码
git clone https://github.com/gumengkai/db_monitor

#### 安装依赖包
pip install -r requirements.txt

#### settings配置
--MySQL数据库：

DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
		'NAME': 'db_monitor',  
		'USER': 'root',  
		'PASSWORD': 'mysqld',  
        'HOST':'127.0.0.1',  
		'PORT': '3306',  
    }
}

--Redis：

CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

CELERY_BROKER_URL = 'redis://localhost:6379/2'

--邮件告警配置：

IS_SEND_EAMIL = 0 #是否发送告警邮件，0：不发送 1：发送

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #一般不需要修改

EMAIL_HOST = 'smtp.163.com'

EMAIL_PORT = 25

EMAIL_HOST_USER = '*********'    # 邮箱登录名，如11111111111@163.com

EMAIL_HOST_PASSWORD = '*********'   #此处为客户端授权码，不是邮箱密码，需要在邮箱服务商设置

EMAIL_TO_USER = ['1782365880@qq.com','gumengkai@hotmail.com'] # 发送邮件列表,参考格式设置

--钉钉告警配置

IS_SEND_DING_MSG = 0  #是否发送钉钉告警 0：不发送 1：发送

DING_WEBHOOK = '**********' #webhook，从钉钉获取

#### 创建数据库
python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser(创建登录用户)

#### 执行数据库脚本

@install/initdata.sql

初始化脚本包含celery初始数据和admin初始用户(密码为111111)

### 6. 启动/停止
python manage.py runserver 0.0.0.0:8000 #建议使用固定IP地址启动

celery –A db_monitor worker –l info

celery –A db_monitor beat –l info

也可以使用脚本启动/关闭：

celery: sh celery_start[shutdown].sh

django: sh web_start[shutdown].sh

关于日志：

celery日志：logs/celery-worker.log & logs/celery-beat.log

web日志： logs/django-web.log

采集数据异常主要查看celery日志！

注：使用shell脚本启停时如遇到“/r command not found”，为linux与windows换行符格式差异导致，在Linux凭条可以在vim下执行:set ff=unix解决

### 7. 前端配置
请参考：[db_monitor_vue](https://github.com/gumengkai/db_monitor_vue)

### 8. oracle数据库监控
对Oracle数据库监控，请在被监控端建立用户，并执行install/sqlscripts(forOracle)中的脚本

grant.sql & table.sql & procedure.sql

### 9. 数据库部署
--Oracle数据库部署(仅支持19c版本)

若要使用"数据库部署"的功能，需要手工下载数据库安装包并拷贝到utils/oracle_rac_install/目录中。

LINUX.X64_193000_grid_home.zip --安装集群需要，只安装单实例则不需要

LINUX.X64_193000_db_home.zip

注：安装前需要提前准备的
1. 配置yum源
2. 网卡配置(rac安装)，包括private,public网络配置
3. 服务器的配置应满足官方安装要求，如物理内存、磁盘空间、swap，自动化安装程序并不会对这些进行检查
4. 共享磁盘配置(rac安装)，需要在完成step1 linux配置后进行共享存储配置，才可继续进行后续grid安装

--MySQL数据库部署(支持5.7/8.0版本)
需要手工下载数据库安装包并拷贝到utils/mysql_install/目录中。
mysql-5.7.33-linux-glibc2.12-x86_64.tar.gz 

mysql-8.0.23-linux-glibc2.12-x86_64.tar.xz


### 10. 访问地址
取决于自己的前端和后端端口配置，默认访问地址为

ip:8000/admin --后端

ip:8001 --前端

### 11. 系统设置
如采集频率，可在django后台管理页面进行配置
![demo1](images/demo8.jpg)

## 界面展示

- 资产管理

![demo1](images/demo1.jpg)

- Oracle数据库概览

![demo1](images/demo2.jpg)

- oracle top sql

![demo1](images/demo6.jpg)

- MySQL数据库日志解析

![demo1](images/demo3.jpg)

- 告警记录

![demo1](images/demo4.jpg)

- 告警配置

![demo1](images/demo5.jpg)

- 数据库部署

![demo1](images/demo7.jpg)

## 交流学习
- QQ群 916746047

另外，安装过程中出现的问题可优先查看此文档：
https://docs.qq.com/doc/DZHlBSGFGd1lpWUVS

docker部署可参考：
https://blog.csdn.net/gumengkai/article/details/106250548

Copyright © 2019 DB monitor



#coding: utf-8

import os
from django.core.mail import send_mail
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'db_monitor.settings'

def my_send_email(header,content):
    from_user = settings.EMAIL_HOST_USER
    to_user = settings.EMAIL_TO_USER
    is_send = settings.IS_SEND_EMAIL
    if is_send == 1:
        send_mail(header, content, from_user, to_user, )



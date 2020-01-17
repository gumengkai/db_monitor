#! /bin/bash
python manage.py makemigrations &&
python manage.py migrate &&
python manage.py runserver 127.0.0.1:8080 > django-web.log 2>&1 &

celery multi start w1 -A db_monitor -l info
celery -A db_monitor beat -l info >  celery-beat.log  2>&1  &



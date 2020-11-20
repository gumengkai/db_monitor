ps auxww | grep 'celery'|grep 'db_monitor' | awk '{print $2}' | xargs kill -9

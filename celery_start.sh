celery multi start w1 -A otcops -l info --logfile=logs/celery-worker.log --pidfile=celery-worker.pid
celery -A otcops beat -l info >  logs/celery-beat.log  2>&1  &

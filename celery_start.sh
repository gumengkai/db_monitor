rm -rf *.pid
export PYTHONOPTIMIZE=1
celery multi start w1 -A db_monitor -l info --logfile=logs/celery-worker.log --pidfile=celery-worker.pid
celery -A db_monitor beat -l info >  logs/celery-beat.log  2>&1  &

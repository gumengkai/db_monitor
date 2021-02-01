python manage.py makemigrations &&
python manage.py migrate &&
python manage.py runserver 0.0.0.0:8001 > logs/django-web.log 2>&1 &

web: python manage.py migrate --noinput && waitress-serve --port=$PORT conf.wsgi:application
celery_worker: celery -A conf worker -l info
celery_beat: celery -A conf beat -l info -S django

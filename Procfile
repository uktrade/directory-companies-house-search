web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && waitress-serve --port=$PORT chsearch.wsgi:application
celery_worker: celery -A chsearch worker -l info
celery_beat: celery -A chsearch beat -l info -S django

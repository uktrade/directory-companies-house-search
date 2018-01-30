web: python manage.py distributed_migrate --noinput && python manage.py collectstatic --noinput && waitress-serve --port=$PORT chsearch.wsgi:application

#!/bin/bash -xe

python /usr/src/app/manage.py distributed_migrate --noinput
python /usr/src/app/manage.py distributed_elasticsearch_migrate
python /usr/src/app/manage.py collectstatic --noinput
gunicorn chsearch.wsgi --bind 0.0.0.0:$PORT --log-file -

#!/bin/bash -xe

celery -A chsearch beat -l info -S django

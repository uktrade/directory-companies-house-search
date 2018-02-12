#!/bin/bash -xe

celery -A chsearch worker -l info

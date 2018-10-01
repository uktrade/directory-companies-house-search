from django.core.cache import cache
from django.core.management import call_command

from conf.celery import app


def lock_acquired(lock_name):
    """ Returns False if the lock was already set in the last 20 hours
    Multiple celery beat schedulers are running at the same time, which
    results in duplicated scheduled tasks. Cache-lock mechanism is used to
    assure that only one task gets executed. Lock expires after 20 hours
    """
    return cache.add(lock_name, 'acquired', 72000)


@app.task
def import_ch_companies():
    if lock_acquired('import_ch_companies'):
        call_command('import_ch_companies')

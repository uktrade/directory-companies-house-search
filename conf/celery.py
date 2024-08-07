from __future__ import absolute_import, unicode_literals
import os
import ssl

from celery import Celery
from dbt_copilot_python.celery_health_check import healthcheck

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

app = Celery(
    "conf",
)

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

ssl_conf = {
    "ssl_cert_reqs": ssl.CERT_NONE,
    "ssl_ca_certs": None,
    "ssl_certfile": None,
    "ssl_keyfile": None,
}
app.conf.broker_use_ssl = ssl_conf
app.conf.redis_backend_use_ssl = ssl_conf

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app = healthcheck.setup(app)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

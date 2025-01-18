from __future__ import absolute_import, unicode_literals
import logging
import os
from logging.config import dictConfig
from celery.signals import setup_logging
from celery import Celery
from celery import signals
from django.conf import settings

# Set default Django settings module for 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adwise.settings")

# Create Celery app
app = Celery("adwise")

# Load task modules from all registered Django app configs
app.config_from_object("django.conf:settings", namespace="CELERY")


@setup_logging.connect
def config_loggers(*args, **kwargs):
    dictConfig(settings.LOGGING)


# Autodiscover tasks from installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@signals.worker_shutdown.connect
def handle_worker_shutdown(*args, **kwargs):
    for handler in logging.getLogger().handlers:
        handler.close()
        logging.getLogger().removeHandler(handler)

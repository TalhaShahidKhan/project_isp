from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ispms.settings')

app = Celery('ispms')




app.conf.beat_schedule = {
    'subs_check': {
        'task': 'subscription.tasks.check_active',
        'schedule': crontab(minute=0, hour=0),
    },
    'cus_chec': {
        'task': 'customer.tasks.customer_active',
        'schedule': crontab(minute=0, hour=0),
    },
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
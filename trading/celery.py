from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading.settings')

app = Celery('trading')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings,namespace='CELERY')

# app.autodiscover_tasks(['stratergy'])
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
app.autodiscover_tasks()

from celery.schedules import crontab

from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    'update_data_task': {
        'task': 'strategy.tasks.update_data',
        'schedule': timedelta(seconds=3600),  # Run every 1 hour
    },
}


#app.conf.beat_schedule = {
#    "send-price-updates" : {
#        'task':'stratergy.tasks.update_data',
#       'schedule' : crontab(hour=18,minute=05),
#    }
#}



@app.task(bind=True)
def debug_task(self):
    print('debuging ...')
    print(f"Request: {self.request!r}")


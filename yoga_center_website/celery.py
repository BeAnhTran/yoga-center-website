import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yoga_center_website.settings')

app = Celery('yoga_center_website')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Calls test every 30 seconds
    'test-notify-unpaid-card-every-30-seconds': {
        'task': 'apps.common.tasks.notify_unpaid_card',
        'schedule': 30.0,
    },
    # Executes every Monday morning at 10:00 a.m.
    'notify-unpaid-card-every-10am-morning': {
        'task': 'apps.common.tasks.notify_unpaid_card',
        'schedule': crontab(hour=12, minute=0),
    },
}

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yoga_center_website.settings')

app = Celery('yoga_center_website')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

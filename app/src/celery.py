import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app_celery = Celery('picasso')

app_celery.config_from_object('django.conf:settings', namespace='CELERY')

app_celery.autodiscover_tasks()

import os

from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'articlegenerator.settings')

from django.conf import settings


app = Celery('article')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)

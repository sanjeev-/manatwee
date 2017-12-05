import os
from celery import Celery

print celery.__file__

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manatwee.settings')

app = Celery('manatwee')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
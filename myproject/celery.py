import os
from celery import Celery
from celery.schedules import cronfield, crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'myapp.tasks.add',
        'schedule': 30.0,
        'args':(38,23)
    },
    'run-every-midnight': {
        'task': 'myapp.tasks.sheduled_task',
        'schedule': 60.0
    }
}
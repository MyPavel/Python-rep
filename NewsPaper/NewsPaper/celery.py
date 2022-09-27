import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'news.tasks.my_mail',
        'schedule': crontab(minute='0', hour='8', day_of_week='monday'),

    },
}

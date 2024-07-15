from celery import Celery
from django.conf import settings
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('django_project', broker_url='amqp://guest:guest@localhost:5672/')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'delete-old-posts-every-5-minutes': {
        'task': 'posts.tasks.delete_old_posts',
        'schedule': 30.0,  # Every 30 seconds
    },
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

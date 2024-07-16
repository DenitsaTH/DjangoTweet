from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('django_project', broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'delete-old-posts-every-5-minutes': {
        'task': 'posts.tasks.delete_old_posts',
        'schedule': 30.0,  # Every 30 seconds for testing
    },
}

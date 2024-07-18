from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from posts.models import Post


@shared_task
def delete_old_posts():
    print(f"Running task at {timezone.now()}")

    threshold = timezone.now() - timedelta(seconds=30)
    deleted_posts = Post.objects.filter(is_deleted=True, deleted_at__lte=threshold)

    print(f"Found {deleted_posts.count()} posts to delete")

    deleted_posts.delete()
    
    print("Old posts deleted")

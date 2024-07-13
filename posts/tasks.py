from django.utils import timezone
from background_task import background

from posts.models import Post


# scheduled to run after 5 seconds -> for testing purposes
@background(schedule=5)
def delete_posts():

    # switch days=10 with seconds=5 to test this
    ten_days_ago = timezone.now() - timezone.timedelta(days=10)

    soft_deleted_posts = Post.objects.filter(is_deleted=True, 
                                                 deleted_at__lte=ten_days_ago)
        
    soft_deleted_posts.delete()

from datetime import timezone
from django.db import models

from users.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


    def delete(self):
        self.posts.all().update(is_deleted=True, deleted_at=timezone.now())
        super().delete()


    @property
    def liked_users(self):
        return self.likes.all()
    
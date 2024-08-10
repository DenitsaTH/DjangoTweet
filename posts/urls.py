from django.urls import path

from posts.api import get_posts, submit_post, switch_like, delete_post

app_name = 'posts'

urlpatterns = [
    path('home/', get_posts, name='get_all_posts'),
    path('posts/', submit_post, name='submit_post'),
    path('posts/<int:post_id>/likes/', switch_like, name='switch_post_like'),
    path('users/posts/<int:post_id>/', delete_post, name='delete_post'),
]

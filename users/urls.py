from django.urls import path

from users.api import (
    home_page,
    register,
    logout,
    update_profile,
    update_profile_picture,
    get_user_likes_and_posts,
)

app_name = 'users'

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register),
    path('logout/', logout),
    path('users/profile/', update_profile, name='update_profile'),
    path(
        'users/profile/picture/',
        update_profile_picture,
        name='profile_picture_upload',
    ),
    path(
        'users/posts/',
        get_user_likes_and_posts,
        name='get_total_posts_and_post_likes',
    ),
]

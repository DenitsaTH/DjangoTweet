from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from posts import api as posts_api
from users import api as users_api


schema_view = get_schema_view(
    openapi.Info(
        title='Swagger docs',
        default_version='v1',
        description='API documentation',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'google-oauth2/login/',
        include('authentication.urls', namespace='authentication'),
    ),
    path('register/', users_api.register),
    path('logout/', users_api.logout),
    path('home/', posts_api.get_posts, name='get_all_posts'),
    path('users/profile/', users_api.update_profile, name='update_profile'),
    path(
        'users/profile/picture/',
        users_api.update_profile_picture,
        name='profile_picture_upload',
    ),
    path(
        'users/posts/',
        users_api.get_user_likes_and_posts,
        name='get_total_posts_and_post_likes',
    ),
    path('users/posts/<int:post_id>/', posts_api.delete_post, name='delete_post'),
    path('posts/', posts_api.submit_post, name='submit_post'),
    path('posts/<int:post_id>/likes/', posts_api.switch_like, name='switch_post_like'),
    path('', users_api.home_page, name='home_page'),
    path(
        'api/v1/swagger/schema/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger',
    ),
]

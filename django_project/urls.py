from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


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
    path(
        '',
        include('posts.urls', namespace='posts'),
    ),
    path(
        '',
        include('users.urls', namespace='users'),
    ),
    path(
        'api/v1/swagger/schema/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger',
    ),
]

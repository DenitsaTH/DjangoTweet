from django.urls import path

from authentication.api import (
    google_login_api,
    google_login_redirect_api,
)

app_name = 'authentication'

urlpatterns = [
    path('callback/', google_login_api, name='callback'),
    path('redirect/', google_login_redirect_api, name='redirect'),
]

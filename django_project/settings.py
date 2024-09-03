"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from django_project.env import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_BACKEND_URL = env.str('DJANGO_BASE_BACKEND_URL', default='http://127.0.0.1:8000')

SECRET_KEY = env.str('SECRET_KEY', default='')

# Switch to False for production
DEBUG = True

# Custom user model used for authentication
AUTH_USER_MODEL = 'users.User'

# The host/domain names that this Django app can serve.
ALLOWED_HOSTS = ['*']

# TIME_ZONE and USE_TZ settings

TIME_ZONE = 'Europe/Sofia'
USE_TZ = True

# Application definition

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    # Third-party Apps
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'background_task',
    # Custom Apps
    'users',
    'posts',
    'authentication',
    'forecast',
]

# Django REST Framework configuration

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# Middleware configuration

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Celery settings
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
# CELERY_RESULT_BACKEND = 'django-db'


# Django-celery-results configuration
# CELERY_RESULT_BACKEND = 'django-db+mysql://root:proprie@localhost:3306/django'
CELERY_RESULT_BACKEND = 'db+sqlite:///db.sqlite3'


# Media files (uploads)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# CORS settings

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# URL configuration

ROOT_URLCONF = 'django_project.urls'


# Templates configuration

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# WSGI application

WSGI_APPLICATION = 'django_project.wsgi.application'


# Database configuration

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'django',
#         'USER': 'root',
#         'PASSWORD': 'proprie',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'
USE_I18N = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Swagger settings

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}


# Google Authentication

GOOGLE_OAUTH2_CLIENT_ID = env.str('DJANGO_GOOGLE_OAUTH2_CLIENT_ID', default='')
GOOGLE_OAUTH2_CLIENT_SECRET = env.str('DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET', default='')
GOOGLE_OAUTH2_PROJECT_ID = env.str('DJANGO_GOOGLE_OAUTH2_PROJECT_ID', default='')


# Session Management Settings

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Optional session cookie settings for local testing
# SESSION_COOKIE_NAME = 'my_session_id'
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Optional CSRF cookie settings (adjust for security)
# CSRF_COOKIE_HTTPONLY = True

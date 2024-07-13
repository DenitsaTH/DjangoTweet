from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(blank=True)
    description = models.CharField(max_length=200, blank=True)
    is_sandboxed = models.BooleanField(null=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

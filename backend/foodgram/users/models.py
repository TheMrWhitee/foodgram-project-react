from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=20,
                                unique=True,
                                verbose_name='Username')
    email = models.EmailField(max_length=50)
    first_name = models.CharField(max_length=20, verbose_name='First name')
    last_name = models.CharField(max_length=20, verbose_name='Last name')
    is_subscribed = models.BooleanField(default=False, blank=True)

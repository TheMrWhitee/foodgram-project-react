from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Username',
        validators=[RegexValidator(
            regex=r'^[A-Za-z0-9]+$',
            message='Username должен содержать английские буквы и/или цифры'
        )]
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, verbose_name='First name')
    last_name = models.CharField(max_length=150, verbose_name='Last name')
    is_subscribed = models.BooleanField(default=False)


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             null=True)
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='following',
                                  null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'following'],
                       name='unique_follow')]

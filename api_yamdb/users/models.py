from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (

        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),

    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=50, choices = ROLES)
    is_superuser = models.BooleanField(_('superuser status'),
                                       default=False)

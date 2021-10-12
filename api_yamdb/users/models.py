from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (

        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),

    )
    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=50, choices=ROLES, default='user')
    is_superuser = models.BooleanField(_('superuser status'),
                                       default=False)
    is_verified = models.BooleanField(default=False)

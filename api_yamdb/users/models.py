from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin')
]


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=50, choices=ROLES, default=USER)
    is_superuser = models.BooleanField(_('superuser status'),
                                       default=False)
    is_verified = models.BooleanField(default=False)

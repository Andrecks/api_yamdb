from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .validators import UnicodeUsernameValidator

# class NewUser(models.Model):
    
#     username_validator = UnicodeUsernameValidator()
#     username = models.CharField(
#         _('username'),
#         max_length=150,
#         unique=True,
#         help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         validators=[username_validator],
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
#     email = models.EmailField(('email address'), blank=True)

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
    role = models.CharField(max_length=50, choices = ROLES, default='user')
    is_superuser = models.BooleanField(_('superuser status'),
                                       default=False)
    is_verified = models.BooleanField(default=False)
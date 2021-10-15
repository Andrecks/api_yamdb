from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


def my_year_validator(value):
    if value > datetime.now().year:
        raise ValidationError(
            ('Будущее (пока что) не наступило'),
            params={'value': value},
        )


class Title(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    genre = models.ManyToManyField(
        'media.Genres',
        blank=True,
        related_name='titles',
    )
    category = models.ForeignKey(
        'media.Category',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    year = models.IntegerField('Год выпуска',
                               validators=[my_year_validator])

    def __str__(self):
        return self.name


class Review(models.Model):
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        unique_together = ("author", "title")

    def __str__(self):
        return self.text

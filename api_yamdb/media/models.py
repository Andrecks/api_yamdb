from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User
from datetime import datetime

class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    year = datetime.now().year
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    genre = models.ManyToManyField(
        Genres,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    year = models.IntegerField('Год выпуска', 
                               validators=[MaxValueValidator(year)])

    def __str__(self):
        return self.title_name


class Review(models.Model):
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.OneToOneField(
        Titles, on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

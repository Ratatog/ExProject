from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    favorites = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name='Избранное', related_name='favs')
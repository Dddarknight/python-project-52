from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class HexletUser(AbstractUser):
    username = models.TextField(unique=True)

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        url = reverse_lazy('users')
        return f'{url}{self.id}'

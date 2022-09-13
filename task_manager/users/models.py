from django.contrib.auth.models import AbstractUser
from django.db import models


class HexletUser(AbstractUser):
    username = models.TextField(unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
from django.contrib.auth.models import AbstractUser
from django.db import models


class HexletUser(AbstractUser):
    username = models.TextField(unique=True)

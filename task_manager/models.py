from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class HexletUser(AbstractUser):
    username = models.TextField(unique=True)

class Statuses(models.Model):
   name = models.TextField(unique=True)
   created_at = models.DateTimeField(default=timezone.now)

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class HexletUser(AbstractUser):
    username = models.TextField(unique=True)


class Statuses(models.Model):
    name = models.TextField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Tasks(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField(max_length=500)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT)
    author = models.ForeignKey(
        HexletUser, on_delete=models.PROTECT, related_name='author', null=True)
    executor = models.ForeignKey(
        HexletUser, on_delete=models.PROTECT, related_name='executor')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

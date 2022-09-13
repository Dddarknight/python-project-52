from django.db import models
from django.utils import timezone


class Statuses(models.Model):
    name = models.TextField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

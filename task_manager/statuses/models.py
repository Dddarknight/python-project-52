from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy


class Statuses(models.Model):
    name = models.TextField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url = reverse_lazy('statuses')
        return f'{url}{self.id}'

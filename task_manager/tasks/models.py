from django.db import models
from django.utils import timezone
from task_manager.users.models import HexletUser
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


class Tasks(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField(max_length=500)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT)
    author = models.ForeignKey(
        HexletUser, on_delete=models.PROTECT, related_name='author', null=True)
    executor = models.ForeignKey(
        HexletUser,
        on_delete=models.PROTECT,
        related_name='executor',
        null=True)
    created_at = models.DateTimeField(default=timezone.now)
    labels = models.ManyToManyField(Labels, related_name='tasks')

    def __str__(self):
        return self.name

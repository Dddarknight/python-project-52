from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.db import models


class HexletUser(AbstractUser):
    username = models.TextField(unique=True)

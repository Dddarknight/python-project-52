from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.db import models


class MinimumLengthValidator:
    def __init__(self, max_length=150):
        self.max_length = max_length
    
    def validate_username(self, username):
        if len(self.username) > self.max_length:
            raise ValidationError(
                _("Имя пользователя должно содержать не более %(max_length)d символов."),
                code='username_too_long',
                params={'max_length': self.max_length},
            )
    
    def get_help_text(self):
        return _(
            "Имя пользователя должно содержать не более %(max_length)d символов."
            % {'max_length': self.max_length}
        )


class HexletUser(AbstractUser):
    username = models.TextField(unique=True)

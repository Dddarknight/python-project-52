from django.utils.translation import gettext as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect


MESSAGE_LOGGED_OUT = _("Вы разлогинены.")


class MessageLogOutMixin:

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, MESSAGE_LOGGED_OUT)
        return response

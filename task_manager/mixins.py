from django.utils.translation import gettext as _
from django.contrib import messages


MESSAGE_LOGGED_OUT = _("Вы разлогинены.")


class MessageLogOutMixin:

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, MESSAGE_LOGGED_OUT)
        return response

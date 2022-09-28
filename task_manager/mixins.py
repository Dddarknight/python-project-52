from django.utils.translation import gettext as _
from django.contrib import messages


LOGGED_OUT_MESSAGE = _("Вы разлогинены.")


class MessageLogOutMixin:

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, LOGGED_OUT_MESSAGE)
        return response

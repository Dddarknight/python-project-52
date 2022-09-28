from django.utils.translation import gettext as _
from task_manager.tasks.models import Tasks
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


STATUS_DELETE_DENIED_MESSAGE = _("Невозможно удалить статус, "
                                 "потому что он используется")


class StatusWithTaskCheckMixin:

    def form_valid(self, form):
        if Tasks.objects.all().exists():
            if self.kwargs['pk'] in list(
                    Tasks.objects.values_list('status', flat=True)):
                messages.error(self.request, STATUS_DELETE_DENIED_MESSAGE)
                return redirect(reverse_lazy('statuses'))
        valid = super().form_valid(form)
        return valid

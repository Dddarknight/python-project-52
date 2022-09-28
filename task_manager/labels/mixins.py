from django.utils.translation import gettext as _
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


LABEL_DELETE_DENIED_MESSAGE = _("Невозможно удалить метку, "
                                "потому что она используется")


class LabelWithTaskCheckMixin:

    def form_valid(self, form):
        label = Labels.objects.get(id=self.kwargs['pk'])
        for task in Tasks.objects.all():
            if label in task.labels.all():
                messages.error(self.request, LABEL_DELETE_DENIED_MESSAGE)
                return redirect(reverse_lazy('labels'))
        valid = super().form_valid(form)
        return valid

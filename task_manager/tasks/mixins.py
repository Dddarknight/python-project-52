from django.utils.translation import gettext as _
from task_manager.tasks.models import Tasks
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


TASK_DELETE_DENIED_MESSAGE = _("Задачу может удалить только её автор.")


class SetAuthorMixin:

    def form_valid(self, form):
        valid = super().form_valid(form)
        self.object.author = self.request.user
        self.object.save()
        return valid


class TaskDeletePermissionsMixin:

    def form_valid(self, form):
        task = Tasks.objects.get(id=self.kwargs['pk'])
        if self.request.user.id != task.author.id:
            messages.error(self.request, TASK_DELETE_DENIED_MESSAGE)
            return redirect(reverse_lazy('tasks'))
        valid = super().form_valid(form)
        return valid

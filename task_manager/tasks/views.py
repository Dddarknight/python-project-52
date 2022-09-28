from django.utils.translation import gettext as _
from django.views import generic
from task_manager.tasks.forms import TaskCreationForm
from task_manager.tasks.forms import TaskFilter
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.tasks.models import Tasks
from django_filters.views import FilterView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.tasks.mixins import SetAuthorMixin
from task_manager.tasks.mixins import TaskDeletePermissionsMixin


TASK_CREATE_SUCCESS_MESSAGE = _("Задача успешно создана")
TASK_UPDATE_SUCCESS_MESSAGE = _("Задача успешно изменена")
TASK_DELETE_SUCCESS_MESSAGE = _("Задача успешно удалена")


class TasksView(FilterView):
    template_name = 'tasks/tasks_filter.html'
    model = Tasks
    filterset_class = TaskFilter


class TaskCreateView(SuccessMessageMixin,
                     SetAuthorMixin,
                     CreateView):
    template_name = 'tasks/task_create.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks')
    success_message = TASK_CREATE_SUCCESS_MESSAGE


class TaskUpdateView(SuccessMessageMixin,
                     LoginRequiredMixin,
                     UpdateView):
    model = Tasks
    template_name = 'tasks/task_update.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks')
    success_message = TASK_UPDATE_SUCCESS_MESSAGE
    login_url = reverse_lazy('login')
    redirect_field_name = None


class TaskDeleteView(TaskDeletePermissionsMixin,
                     SuccessMessageMixin,
                     LoginRequiredMixin,
                     DeleteView):
    model = Tasks
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = TASK_DELETE_SUCCESS_MESSAGE
    login_url = reverse_lazy('login')
    redirect_field_name = None


class TaskDescriptionView(generic.TemplateView):
    template_name = 'tasks/task_description.html'

    def get(self, request, **kwargs):
        task = Tasks.objects.get(id=kwargs['pk'])
        return render(
            request, self.template_name, {'task': task,
                                          'labels': task.labels.all()})

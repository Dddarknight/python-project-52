from django.utils.translation import gettext as _
from task_manager.statuses.forms import StatusCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.statuses.models import Statuses
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.statuses.mixins import StatusWithTaskCheckMixin


STATUS_CREATE_SUCCESS_MESSAGE = _("Статус успешно создан")
STATUS_UPDATE_SUCCESS_MESSAGE = _("Статус успешно изменён")
STATUS_DELETE_SUCCESS_MESSAGE = _("Статус успешно удалён")


class StatusesView(ListView):
    template_name = 'statuses/statuses.html'
    model = Statuses


class StatusCreateView(SuccessMessageMixin, CreateView):
    template_name = 'statuses/status_create.html'
    form_class = StatusCreationForm
    success_url = reverse_lazy('statuses')
    success_message = STATUS_CREATE_SUCCESS_MESSAGE


class StatusUpdateView(SuccessMessageMixin,
                       LoginRequiredMixin,
                       UpdateView):
    model = Statuses
    template_name = 'statuses/status_update.html'
    form_class = StatusCreationForm
    success_url = reverse_lazy('statuses')
    success_message = STATUS_UPDATE_SUCCESS_MESSAGE
    login_url = reverse_lazy('login')
    redirect_field_name = None


class StatusDeleteView(StatusWithTaskCheckMixin,
                       SuccessMessageMixin,
                       LoginRequiredMixin,
                       DeleteView):
    model = Statuses
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses')
    success_message = STATUS_DELETE_SUCCESS_MESSAGE
    login_url = reverse_lazy('login')
    redirect_field_name = None

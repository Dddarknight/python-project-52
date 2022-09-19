from django.utils.translation import gettext as _
from task_manager.labels.forms import LabelCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.labels.models import Labels
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.labels.mixins import LabelWithTaskCheckMixin


MESSAGE_LABEL_CREATE_SUCCESS = _("Метка успешно создана")
MESSAGE_LABEL_UPDATE_SUCCESS = _("Метка успешно изменена")
MESSAGE_LABEL_DELETE_SUCCESS = _("Метка успешно удалена")


class LabelsView(ListView):
    template_name = 'labels/labels.html'
    model = Labels


class LabelCreateView(SuccessMessageMixin, CreateView):
    template_name = 'labels/label_create.html'
    form_class = LabelCreationForm
    success_url = reverse_lazy('labels')
    success_message = MESSAGE_LABEL_CREATE_SUCCESS


class LabelUpdateView(SuccessMessageMixin,
                      LoginRequiredMixin,
                      UpdateView):
    model = Labels
    template_name = 'labels/label_update.html'
    form_class = LabelCreationForm
    success_url = reverse_lazy('labels')
    success_message = MESSAGE_LABEL_UPDATE_SUCCESS
    login_url = reverse_lazy('login')
    redirect_field_name = None


class LabelDeleteView(LabelWithTaskCheckMixin,
                      SuccessMessageMixin,
                      LoginRequiredMixin,
                      DeleteView):
    model = Labels
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels')
    success_message = MESSAGE_LABEL_DELETE_SUCCESS
    login_url = reverse_lazy('login')
    redirect_field_name = None

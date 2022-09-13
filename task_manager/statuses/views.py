from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic.edit import FormView
from task_manager.statuses.forms import StatusCreationForm, StatusUpdateForm
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib import messages
from task_manager.users.views import check_authentication


MESSAGE_STATUS_CREATE_SUCCESS = _("Статус успешно создан")
MESSAGE_STATUS_UPDATE_SUCCESS = _("Статус успешно изменён")
MESSAGE_STATUS_DELETE_SUCCESS = _("Статус успешно удалён")
MESSAGE_STATUS_DELETE_DENIED = _("Невозможно удалить статус, "
                                 "потому что он используется")


class StatusesView(ListView):
    template_name = 'statuses/statuses.html'
    model = Statuses

    def get(self, request):
        check_authentication(request)
        return render(request, self.template_name, {
            'object_list': self.model.objects.all()})


class StatusCreationFormView(FormView):
    template_name = 'statuses/status_create.html'
    form_class = StatusCreationForm

    def post(self, request):
        form = self.form_class(request.POST)
        names = list(Statuses.objects.values_list('name', flat=True))
        if form.data['name'] not in names:
            form.save()
            messages.success(request, MESSAGE_STATUS_CREATE_SUCCESS)
            return redirect('statuses')
        return render(request, self.template_name, {
            'form': form, 'failed': 'failed'})

    def get(self, request):
        check_authentication(request)
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class UpdateStatusView(FormView):
    template_name = 'statuses/status_update.html'
    form_class = StatusUpdateForm

    def post(self, request, **kwargs):
        status = Statuses.objects.get(id=kwargs['pk'])
        old_status_name = status.name
        form = self.form_class(request.POST, instance=status)
        names = list(Statuses.objects.values_list('name', flat=True))
        if form.data['name'] not in names or (
                form.data['name'] == old_status_name):
            form.save()
            messages.success(request, MESSAGE_STATUS_UPDATE_SUCCESS)
            return redirect('statuses')
        return render(request, self.template_name, {
            'form': form, 'failed': 'failed'})

    def get(self, request, **kwargs):
        check_authentication(request)
        form = self.form_class(initial=self.initial)
        form.fields['name'].initial = Statuses.objects.get(
            id=kwargs['pk']).name
        return render(request, self.template_name, {'form': form})


class DeleteStatusView(generic.TemplateView):
    template_name = 'statuses/status_delete.html'

    def post(self, request, **kwargs):
        status = Statuses.objects.get(id=kwargs['pk'])
        if status.id in list(Tasks.objects.values_list('status', flat=True)):
            messages.error(request, MESSAGE_STATUS_DELETE_DENIED)
            return redirect('statuses')
        status.delete()
        messages.success(request, MESSAGE_STATUS_DELETE_SUCCESS)
        return redirect('statuses')

    def get(self, request, **kwargs):
        status = Statuses.objects.get(id=kwargs['pk'])
        check_authentication(request)

        return render(request, self.template_name, {'status': status})

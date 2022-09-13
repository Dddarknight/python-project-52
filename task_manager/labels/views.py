from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic.edit import FormView
from task_manager.labels.forms import LabelCreationForm, LabelUpdateForm
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib import messages
from task_manager.users.views import check_authentication


MESSAGE_LABEL_CREATE_SUCCESS = _("Метка успешно создана")
MESSAGE_LABEL_UPDATE_SUCCESS = _("Метка успешно изменена")
MESSAGE_LABEL_DELETE_SUCCESS = _("Метка успешно удалена")
MESSAGE_LABEL_DELETE_DENIED = _("Невозможно удалить метку, "
                                "потому что она используется")


class LabelsView(ListView):
    template_name = 'labels/labels.html'
    model = Labels

    def get(self, request):
        check_authentication(request)
        return render(request, self.template_name, {
            'object_list': self.model.objects.all()})


class LabelCreationFormView(FormView):
    template_name = 'labels/label_create.html'
    form_class = LabelCreationForm

    def post(self, request):
        form = self.form_class(request.POST)
        names = list(Labels.objects.values_list('name', flat=True))
        if form.data['name'] not in names:
            form.save()
            messages.success(request, MESSAGE_LABEL_CREATE_SUCCESS)
            return redirect('labels')
        return render(request, self.template_name, {
            'form': form, 'failed': 'failed'})

    def get(self, request):
        check_authentication(request)
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class UpdateLabelView(FormView):
    template_name = 'labels/label_update.html'
    form_class = LabelUpdateForm

    def post(self, request, **kwargs):
        label = Labels.objects.get(id=kwargs['pk'])
        old_label_name = label.name
        form = self.form_class(request.POST, instance=label)
        names = list(Labels.objects.values_list('name', flat=True))
        if form.data['name'] not in names or (
                form.data['name'] == old_label_name):
            form.save()
            messages.success(request, MESSAGE_LABEL_UPDATE_SUCCESS)
            return redirect('labels')
        return render(request, self.template_name, {
            'form': form, 'failed': 'failed'})

    def get(self, request, **kwargs):
        check_authentication(request)
        form = self.form_class(initial=self.initial)
        form.fields['name'].initial = Labels.objects.get(id=kwargs['pk']).name
        return render(request, self.template_name, {'form': form})


class DeleteLabelView(generic.TemplateView):
    template_name = 'labels/label_delete.html'

    def post(self, request, **kwargs):
        label = Labels.objects.get(id=kwargs['pk'])
        for task in Tasks.objects.all():
            if label in task.labels.all():
                messages.error(request, MESSAGE_LABEL_DELETE_DENIED)
                return redirect('labels')
        label.delete()
        messages.success(request, MESSAGE_LABEL_DELETE_SUCCESS)
        return redirect('labels')

    def get(self, request, **kwargs):
        label = Labels.objects.get(id=kwargs['pk'])
        check_authentication(request)
        return render(request, self.template_name, {'label': label})

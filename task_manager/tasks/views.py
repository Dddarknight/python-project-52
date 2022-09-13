from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic.edit import FormView
from task_manager.tasks.forms import TaskCreationForm, TaskUpdateForm
from task_manager.tasks.forms import TaskFilter
from task_manager.users.models import HexletUser
from task_manager.tasks.models import Tasks
from django.shortcuts import render, redirect
from django.contrib import messages
from django_filters.views import FilterView
from django.db.models import Q
from task_manager.users.views import check_authentication


MESSAGE_TASK_CREATE_SUCCESS = _("Задача успешно создана")
MESSAGE_TASK_UPDATE_SUCCESS = _("Задача успешно изменена")
MESSAGE_TASK_DELETE_SUCCESS = _("Задача успешно удалена")
MESSAGE_TASK_DELETE_DENIED = _("Задачу может удалить только её автор.")


class TasksView(FilterView):
    template_name = 'tasks/tasks_filter.html'
    model = Tasks
    filterset_class = TaskFilter


class TaskCreationFormView(FormView):
    template_name = 'tasks/task_create.html'
    form_class = TaskCreationForm

    def post(self, request):
        form = self.form_class(request.POST)
        names = list(Tasks.objects.values_list('name', flat=True))
        if form.data['name'] not in names:
            task = form.save(commit=False)
            task.author = HexletUser.objects.get(id=request.user.id)
            task.save()
            task.labels.set(request.POST.getlist('labels'))
            form.save_m2m()
            messages.success(request, MESSAGE_TASK_CREATE_SUCCESS)
            return redirect('tasks')
        return render(request, self.template_name, {
            'form': form, 'failed': 'failed'})

    def get(self, request):
        check_authentication(request)
        form = self.form_class(initial=self.initial)
        if HexletUser.objects.filter(is_superuser=True):
            form.fields['executor'].queryset = HexletUser.objects.exclude(
                Q(is_superuser=True))
        return render(request, self.template_name, {'form': form})


class UpdateTaskView(FormView):
    template_name = 'tasks/task_update.html'
    form_class = TaskUpdateForm

    def post(self, request, **kwargs):
        task = Tasks.objects.get(id=kwargs['pk'])
        old_task_name = task.name
        form = self.form_class(request.POST, instance=task)
        names = list(Tasks.objects.values_list('name', flat=True))
        if form.data['name'] not in names or (
                form.data['name'] == old_task_name):
            form.save()
            messages.success(request, MESSAGE_TASK_UPDATE_SUCCESS)
            return redirect('tasks')
        return render(request, self.template_name, {
            'form': form, 'failed': 'failed'})

    def get(self, request, **kwargs):
        check_authentication(request)
        form = self.form_class(initial=self.initial)
        form.fields['name'].initial = Tasks.objects.get(
            id=kwargs['pk']).name
        form.fields['description'].initial = Tasks.objects.get(
            id=kwargs['pk']).description
        form.fields['status'].initial = Tasks.objects.get(
            id=kwargs['pk']).status.name
        form.fields['executor'].initial = Tasks.objects.get(
            id=kwargs['pk']).executor
        form.fields['labels'].initial = Tasks.objects.get(
            id=kwargs['pk']).labels.all()
        return render(request, self.template_name, {'form': form})


class DeleteTaskView(generic.TemplateView):
    template_name = 'tasks/task_delete.html'

    def post(self, request, **kwargs):
        task = Tasks.objects.get(id=kwargs['pk'])
        if request.user.id != task.author.id:
            messages.error(
                request, MESSAGE_TASK_DELETE_DENIED)
            return redirect('tasks')
        task.delete()
        messages.success(request, MESSAGE_TASK_DELETE_SUCCESS)
        return redirect('tasks')

    def get(self, request, **kwargs):
        check_authentication(request)
        task = Tasks.objects.get(id=kwargs['pk'])
        author = task.author
        if request.user.id != author.id:
            messages.error(
                request, MESSAGE_TASK_DELETE_DENIED)
            return redirect('tasks')
        return render(request, self.template_name, {'task': task})


class TaskDescriptionView(generic.TemplateView):
    template_name = 'tasks/task_description.html'

    def get(self, request, **kwargs):
        check_authentication(request)
        task = Tasks.objects.get(id=kwargs['pk'])
        return render(
            request, self.template_name, {'task': task,
                                          'labels': task.labels.all()})

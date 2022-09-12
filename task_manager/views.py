from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic.edit import FormView
from task_manager.forms import UserRegistrationForm, HexletLoginForm
from task_manager.forms import HexletUserChangeForm
from task_manager.forms import StatusCreationForm, StatusUpdateForm
from task_manager.forms import TaskCreationForm, TaskUpdateForm
from task_manager.forms import LabelCreationForm, LabelUpdateForm
from task_manager.forms import TaskFilter
from task_manager.models import HexletUser, Statuses, Tasks, Labels
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django_filters.views import FilterView
from django.db.models import Q


def check_authentication(request):
    if not request.user.is_authenticated:
        messages.error(
            request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('login')


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request):
        return render(
            request, self.template_name, {
                'authenticated': request.user.is_authenticated})


class UserRegistrationFormView(FormView):
    template_name = 'registration.html'
    form_class = UserRegistrationForm

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        if username in list(
                HexletUser.objects.values_list('username', flat=True)):
            return render(
                request,
                self.template_name,
                {'form': form, 'failed': 'failed'})
        if form.is_valid():
            form.save()
            messages.success(
                request, _("Пользователь успешно зарегистрирован"))
            return redirect('login')
        messages.error(request, _("При регистрации произошла ошибка"))
        return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class UsersView(ListView):
    template_name = 'users.html'
    model = HexletUser

    def get(self, request):
        return render(request, self.template_name, {
            'authenticated': request.user.is_authenticated,
            'object_list': self.model.objects.all()})


class HexletLoginView(LoginView):
    template_name = 'login.html'
    form_class = HexletLoginForm

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _("Вы залогинены"))
            return redirect('/')
        messages.error(request, _("Пожалуйста, введите правильные имя"
                                  " пользователя и пароль. Оба поля "
                                  "могут быть чувствительны к регистру."))
        return render(request, self.template_name)

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class HexletLogoutView(generic.TemplateView):
    template_name = 'logout.html'

    def get(self, request):
        logout(request)
        messages.success(request, _("Вы разлогинены."))
        return redirect('index')


class UpdateView(FormView):
    template_name = 'update.html'
    form_class = HexletUserChangeForm

    def post(self, request, **kwargs):
        user = HexletUser.objects.get(id=kwargs['pk'])
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, _("Пользователь успешно изменён"))
            return redirect('users')

    def get(self, request, **kwargs):
        check_authentication(request)
        if not request.user.id == kwargs['pk']:
            messages.error(
                request, _(
                    "У вас нет прав для изменения другого пользователя."))
            return redirect('users')
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})


class DeleteView(generic.TemplateView):
    template_name = 'delete.html'

    def post(self, request, **kwargs):
        user = HexletUser.objects.get(id=kwargs['pk'])
        if user.id in list(
            Tasks.objects.values_list('executor', flat=True)) or (
            user.id in list(Tasks.objects.values_list('author', flat=True))
        ):
            messages.error(
                request, _("Невозможно удалить пользователя, "
                           "потому что он используется"))
            return redirect('users')
        user.delete()
        messages.success(request, _("Пользователь успешно удалён"))
        return redirect('users')

    def get(self, request, **kwargs):
        user = HexletUser.objects.get(id=kwargs['pk'])
        check_authentication(request)
        if not request.user.id == kwargs['pk']:
            messages.error(
                request, _(
                    "У вас нет прав для изменения другого пользователя."))
            return redirect('users')
        return render(request, self.template_name, {'user': user})


class StatusesView(ListView):
    template_name = 'statuses.html'
    model = Statuses

    def get(self, request):
        check_authentication(request)
        return render(request, self.template_name, {
            'object_list': self.model.objects.all()})


class StatusCreationFormView(FormView):
    template_name = 'status_create.html'
    form_class = StatusCreationForm

    def post(self, request):
        form = self.form_class(request.POST)
        names = list(Statuses.objects.values_list('name', flat=True))
        if form.data['name'] not in names:
            form.save()
            messages.success(request, _("Статус успешно создан"))
            return redirect('statuses')
        return render(request, self.template_name, {
            'form': form, 'failed': 'failed'})

    def get(self, request):
        check_authentication(request)
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class UpdateStatusView(FormView):
    template_name = 'status_update.html'
    form_class = StatusUpdateForm

    def post(self, request, **kwargs):
        status = Statuses.objects.get(id=kwargs['pk'])
        old_status_name = status.name
        form = self.form_class(request.POST, instance=status)
        names = list(Statuses.objects.values_list('name', flat=True))
        if form.data['name'] not in names or (
                form.data['name'] == old_status_name):
            form.save()
            messages.success(request, _("Статус успешно изменён"))
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
    template_name = 'status_delete.html'

    def post(self, request, **kwargs):
        status = Statuses.objects.get(id=kwargs['pk'])
        if status.id in list(Tasks.objects.values_list('status', flat=True)):
            messages.error(
                request, _("Невозможно удалить статус, "
                           "потому что он используется"))
            return redirect('statuses')
        status.delete()
        messages.success(request, _("Статус успешно удалён"))
        return redirect('statuses')

    def get(self, request, **kwargs):
        status = Statuses.objects.get(id=kwargs['pk'])
        check_authentication(request)

        return render(request, self.template_name, {'status': status})


class TasksView(FilterView):
    template_name = 'task_manager/tasks_filter.html'
    model = Tasks
    filterset_class = TaskFilter


class TaskCreationFormView(FormView):
    template_name = 'task_create.html'
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
            messages.success(request, _("Задача успешно создана"))
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
    template_name = 'task_update.html'
    form_class = TaskUpdateForm

    def post(self, request, **kwargs):
        task = Tasks.objects.get(id=kwargs['pk'])
        old_task_name = task.name
        form = self.form_class(request.POST, instance=task)
        names = list(Tasks.objects.values_list('name', flat=True))
        if form.data['name'] not in names or (
                form.data['name'] == old_task_name):
            form.save()
            messages.success(request, _("Задача успешно изменена"))
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
    template_name = 'task_delete.html'

    def post(self, request, **kwargs):
        task = Tasks.objects.get(id=kwargs['pk'])
        if request.user.id != task.author.id:
            messages.error(
                request, _("Задачу может удалить только её автор."))
            return redirect('tasks')
        task.delete()
        messages.success(request, _("Задача успешно удалена"))
        return redirect('tasks')

    def get(self, request, **kwargs):
        check_authentication(request)
        task = Tasks.objects.get(id=kwargs['pk'])
        author = task.author
        if request.user.id != author.id:
            messages.error(
                request, _("Задачу может удалить только её автор."))
            return redirect('tasks')
        return render(request, self.template_name, {'task': task})


class TaskDescriptionView(generic.TemplateView):
    template_name = 'task_description.html'

    def get(self, request, **kwargs):
        check_authentication(request)
        task = Tasks.objects.get(id=kwargs['pk'])
        return render(
            request, self.template_name, {'task': task,
                                          'labels': task.labels.all()})


class LabelsView(ListView):
    template_name = 'labels.html'
    model = Labels

    def get(self, request):
        check_authentication(request)
        return render(request, self.template_name, {
            'object_list': self.model.objects.all()})


class LabelCreationFormView(FormView):
    template_name = 'label_create.html'
    form_class = LabelCreationForm

    def post(self, request):
        form = self.form_class(request.POST)
        names = list(Labels.objects.values_list('name', flat=True))
        if form.data['name'] not in names:
            form.save()
            messages.success(request, _("Метка успешно создана"))
            return redirect('labels')
        return render(request, self.template_name, {
            'form': form, 'failed': 'failed'})

    def get(self, request):
        check_authentication(request)
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class UpdateLabelView(FormView):
    template_name = 'label_update.html'
    form_class = LabelUpdateForm

    def post(self, request, **kwargs):
        label = Labels.objects.get(id=kwargs['pk'])
        old_label_name = label.name
        form = self.form_class(request.POST, instance=label)
        names = list(Labels.objects.values_list('name', flat=True))
        if form.data['name'] not in names or (
                form.data['name'] == old_label_name):
            form.save()
            messages.success(request, _("Метка успешно изменена"))
            return redirect('labels')
        return render(request, self.template_name, {
            'form': form, 'failed': 'failed'})

    def get(self, request, **kwargs):
        check_authentication(request)
        form = self.form_class(initial=self.initial)
        form.fields['name'].initial = Labels.objects.get(id=kwargs['pk']).name
        return render(request, self.template_name, {'form': form})


class DeleteLabelView(generic.TemplateView):
    template_name = 'label_delete.html'

    def post(self, request, **kwargs):
        label = Labels.objects.get(id=kwargs['pk'])
        for task in Tasks.objects.all():
            if label in task.labels.all():
                messages.error(
                    request, _("Невозможно удалить метку, "
                               "потому что она используется"))
                return redirect('labels')
        label.delete()
        messages.success(request, _("Метка успешно удалена"))
        return redirect('labels')

    def get(self, request, **kwargs):
        label = Labels.objects.get(id=kwargs['pk'])
        check_authentication(request)
        return render(request, self.template_name, {'label': label})

from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic.edit import FormView
from task_manager.users.forms import HexletUserChangeForm
from task_manager.users.forms import UserRegistrationForm
from task_manager.users.models import HexletUser
from task_manager.tasks.models import Tasks
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages


MESSAGE_REGISTRATION_SUCCESS = _("Пользователь успешно зарегистрирован")
MESSAGE_REGISTRATION_ERROR = _("При регистрации произошла ошибка")
MESSAGE_NOT_LOGGED_IN = _("Вы не авторизованы! Пожалуйста, выполните вход.")
MESSAGE_UPDATE_USER_SUCCESS = _("Пользователь успешно изменён")
MESSAGE_CHANGE_USER_DENIED = _("У вас нет прав для изменения "
                               "другого пользователя.")
MESSAGE_DELETE_USER_WITH_TASKS_DENIED = _("Невозможно удалить пользователя, "
                                          "потому что он используется")
MESSAGE_DELETE_SUCCESS = _("Пользователь успешно удалён")


def check_authentication(request):
    if not request.user.is_authenticated:
        messages.error(
            request, MESSAGE_NOT_LOGGED_IN)
        return redirect('login')


class UserRegistrationFormView(FormView):
    template_name = 'users/registration.html'
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
                request, MESSAGE_REGISTRATION_SUCCESS)
            return redirect('login')
        messages.error(request, MESSAGE_REGISTRATION_ERROR)
        return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class UsersView(ListView):
    template_name = 'users/users.html'
    model = HexletUser

    def get(self, request):
        return render(request, self.template_name, {
            'object_list': self.model.objects.all()})


class UpdateView(FormView):
    template_name = 'users/update.html'
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
            messages.success(request, MESSAGE_UPDATE_USER_SUCCESS)
            return redirect('users')

    def get(self, request, **kwargs):
        check_authentication(request)
        if not request.user.id == kwargs['pk']:
            messages.error(request, MESSAGE_CHANGE_USER_DENIED)
            return redirect('users')
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})


class DeleteView(generic.TemplateView):
    template_name = 'users/delete.html'

    def post(self, request, **kwargs):
        user = HexletUser.objects.get(id=kwargs['pk'])
        if user.id in list(
            Tasks.objects.values_list('executor', flat=True)) or (
            user.id in list(Tasks.objects.values_list('author', flat=True))
        ):
            messages.error(request, MESSAGE_DELETE_USER_WITH_TASKS_DENIED)
            return redirect('users')
        user.delete()
        messages.success(request, MESSAGE_DELETE_SUCCESS)
        return redirect('users')

    def get(self, request, **kwargs):
        user = HexletUser.objects.get(id=kwargs['pk'])
        check_authentication(request)
        if not request.user.id == kwargs['pk']:
            messages.error(request, MESSAGE_CHANGE_USER_DENIED)
            return redirect('users')
        return render(request, self.template_name, {'user': user})

from getopt import gnu_getopt
from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic.edit import FormView
from task_manager.forms import UserRegistrationForm, HexletLoginForm
from task_manager.forms import HexletUserChangeForm
from task_manager.models import HexletUser
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout


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
        if form.is_valid():
            form.save()
            messages.success(request, _("Вы успешно зарегистрированы!"))
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
        user = HexletUser.objects.get(id=kwargs['user_id'])
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, _("Ваши данные изменены!"))
            return redirect('users')

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('login')
        if not request.user._get_pk_val() == kwargs['user_id']:
            messages.error(
                request, _(
                    "У вас нет прав для изменения другого пользователя."))
            return redirect('users')
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})


class DeleteView(generic.TemplateView):
    template_name = 'delete.html'

    def post(self, request, **kwargs):
        user = HexletUser.objects.get(id=kwargs['user_id'])
        user.delete()
        messages.success(request, _("Пользователь успешно удалён"))
        return redirect('users')

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('login')
        if not request.user._get_pk_val() == kwargs['user_id']:
            messages.error(
                request, _(
                    "У вас нет прав для изменения другого пользователя."))
            return redirect('users')
        return render(request, self.template_name)

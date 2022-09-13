from django.views import generic
from django.utils.translation import gettext as _
from task_manager.forms import HexletLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout


MESSAGE_LOGGED_IN = _("Вы залогинены")
MESSAGE_LOG_IN_ERROR = _("Пожалуйста, введите правильные имя"
                         " пользователя и пароль. Оба поля "
                         "могут быть чувствительны к регистру.")
MESSAGE_LOGGED_OUT = _("Вы разлогинены.")


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request):
        return render(
            request, self.template_name)


class HexletLoginView(LoginView):
    template_name = 'login.html'
    form_class = HexletLoginForm

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, MESSAGE_LOGGED_IN)
            return redirect('/')
        messages.error(request, MESSAGE_LOG_IN_ERROR)
        return render(request, self.template_name)

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class HexletLogoutView(generic.TemplateView):
    template_name = 'logout.html'

    def get(self, request):
        logout(request)
        messages.success(request, MESSAGE_LOGGED_OUT)
        return redirect('index')

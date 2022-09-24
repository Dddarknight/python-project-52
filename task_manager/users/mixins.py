from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from task_manager.tasks.models import Tasks


MESSAGE_CHANGE_USER_DENIED = _("У вас нет прав для изменения "
                               "другого пользователя.")
MESSAGE_NOT_LOGGED_IN = _("Вы не авторизованы! Пожалуйста, выполните вход.")
MESSAGE_DELETE_USER_WITH_TASKS_DENIED = _("Невозможно удалить пользователя, "
                                          "потому что он используется")


class UserPassesTestMixin_(UserPassesTestMixin):

    def test_func(self):
        if self.kwargs['pk'] != self.request.user.id:
            messages.error(self.request, MESSAGE_CHANGE_USER_DENIED)
            return False
        return True

    def handle_no_permission(request):
        return redirect(reverse_lazy('users'))


class UserPermissionsMixin(LoginRequiredMixin, UserPassesTestMixin_):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, MESSAGE_NOT_LOGGED_IN)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class UserFormLoginMixin:

    def form_valid(self, form):
        valid = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid


class UserWithTaskCheckMixin:

    def form_valid(self, form):
        if self.kwargs['pk'] in list(
            Tasks.objects.values_list('executor', flat=True)) or (
            self.kwargs['pk'] in list(
                Tasks.objects.values_list('author', flat=True))
        ):
            messages.error(self.request, MESSAGE_DELETE_USER_WITH_TASKS_DENIED)
            return redirect(reverse_lazy('users'))
        valid = super().form_valid(form)
        return valid

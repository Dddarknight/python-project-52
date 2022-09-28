from django.utils.translation import gettext as _
from task_manager.users.forms import UserRegistrationForm
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.mixins import UserPermissionsMixin
from task_manager.users.mixins import UserFormLoginMixin
from task_manager.users.mixins import UserWithTaskCheckMixin
from django.urls import reverse_lazy


REGISTRATION_SUCCESS_MESSAGE = _("Пользователь успешно зарегистрирован")
UPDATE_USER_SUCCESS_MESSAGE = _("Пользователь успешно изменён")
DELETE_SUCCESS_MESSAGE = _("Пользователь успешно удалён")


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    success_message = REGISTRATION_SUCCESS_MESSAGE


class UsersView(ListView):
    template_name = 'users/users.html'
    model = get_user_model()


class UserUpdateView(UserPermissionsMixin,
                     SuccessMessageMixin,
                     UserFormLoginMixin,
                     UpdateView):
    model = get_user_model()
    template_name = 'users/update.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users')
    success_message = UPDATE_USER_SUCCESS_MESSAGE
    login_url = reverse_lazy('login')
    redirect_field_name = None


class UserDeleteView(UserPermissionsMixin,
                     UserWithTaskCheckMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = DELETE_SUCCESS_MESSAGE

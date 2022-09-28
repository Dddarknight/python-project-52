from django.views import generic
from django.utils.translation import gettext as _
from task_manager.forms import HexletLoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import MessageLogOutMixin


LOGGED_IN_MESSAGE = _("Вы залогинены")


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class HexletLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = HexletLoginForm
    success_message = LOGGED_IN_MESSAGE


class HexletLogoutView(MessageLogOutMixin, LogoutView):
    pass

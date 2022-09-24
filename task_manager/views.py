from django.views import generic
from django.utils.translation import gettext as _
from task_manager.forms import HexletLoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import MessageLogOutMixin


MESSAGE_LOGGED_IN = _("Вы залогинены")
MESSAGE_LOGGED_OUT = _("Вы разлогинены.")


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class HexletLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = HexletLoginForm
    success_message = MESSAGE_LOGGED_IN


class HexletLogoutView(MessageLogOutMixin, LogoutView):
    pass

from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm
from task_manager.users.models import HexletUser


class HexletLoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Имя пользователя'),
                               label_suffix='',
                               max_length=150,
                               required=True,
                               widget=forms.TextInput(
                                   attrs={'placeholder': _('Имя пользователя'),
                                          'class': 'form-control',
                                          'autofocus': True,
                                          'style': 'max-width: 24em', }))
    password = forms.CharField(label=_('Пароль'),
                               label_suffix='',
                               required=True,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': _('Пароль'),
                                          'class': 'form-control',
                                          'style': 'max-width: 24em', }))

    class Meta:
        model = HexletUser
        fields = ['username', 'password']

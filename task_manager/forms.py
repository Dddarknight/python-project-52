from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


LOG_IN_ERROR_MESSAGE = _("Пожалуйста, введите правильные имя"
                         " пользователя и пароль. Оба поля "
                         "могут быть чувствительны к регистру.")


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
    error_messages = {'invalid_login': LOG_IN_ERROR_MESSAGE}

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

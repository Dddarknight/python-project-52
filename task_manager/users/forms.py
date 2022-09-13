from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import HexletUser


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=_('Имя'),
                                 label_suffix='',
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': _('Имя'),
                                            'class': 'form-control', }))
    last_name = forms.CharField(label=_('Фамилия'),
                                label_suffix='',
                                required=True,
                                widget=forms.TextInput(
                                    attrs={'placeholder': _('Фамилия'),
                                           'class': 'form-control', }))
    username = forms.CharField(label=_('Имя пользователя'),
                               max_length=150,
                               label_suffix='',
                               required=True,
                               help_text=_('Обязательное поле. '
                                           'Не более 150 символов. '
                                           'Только буквы, цифры и '
                                           'символы @/./+/-/_.'),
                               widget=forms.TextInput(
                                   attrs={'placeholder': _('Имя пользователя'),
                                          'autofocus': True,
                                          'class': 'form-control', }))
    password1 = forms.CharField(label=_('Пароль'),
                                label_suffix='',
                                required=True,
                                help_text=_(
                                    "Ваш пароль должен содержать "
                                    "как минимум 3 символа."),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': _('Пароль'),
                                           'class': 'form-control', }))
    password2 = forms.CharField(label=_('Подтверждение пароля'),
                                label_suffix='',
                                required=True,
                                help_text=_("Для подтверждения введите,"
                                            " пожалуйста, пароль ещё раз."),
                                widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': _('Подтверждение '
                                                         'пароля'),
                                        'class': 'form-control', }))

    class Meta:
        model = HexletUser
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2')


class HexletUserChangeForm(UserRegistrationForm):
    pass

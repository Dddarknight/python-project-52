from django import forms
from django.utils.translation import gettext as _
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from task_manager.models import HexletUser, Statuses


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=_('Имя'),
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': _('Имя'),
                                            'class': 'form-control', }))
    last_name = forms.CharField(label=_('Фамилия'),
                                required=True,
                                widget=forms.TextInput(
                                    attrs={'placeholder': _('Фамилия'),
                                           'class': 'form-control', }))
    username = forms.CharField(label=_('Имя пользователя'),
                               max_length=150,
                               required=True,
                               help_text=_('Обязательное поле. '
                                           'Не более 150 символов. '
                                           'Только буквы, цифры и '
                                           'символы @/./+/-/_.'),
                               widget=forms.TextInput(
                                   attrs={'placeholder': _('Имя пользователя'),
                                          'class': 'form-control', }))
    password1 = forms.CharField(label=_('Пароль'),
                                required=True,
                                help_text=_(
                                    "Ваш пароль должен содержать "
                                    "как минимум 3 символа."),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': _('Пароль'),
                                           'class': 'form-control',
                                           'data-toggle': 'password',
                                           'id': 'password', }))
    password2 = forms.CharField(label=_('Подтверждение пароля'),
                                required=True,
                                help_text=_("Для подтверждения введите,"
                                            " пожалуйста, пароль ещё раз."),
                                widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': _('Подтверждение '
                                                         'пароля'),
                                        'class': 'form-control',
                                        'data-toggle': 'password',
                                        'id': 'password', }))

    class Meta:
        model = HexletUser
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2')
        labels = {'first_name': _('Имя'),
                  'last_name': _('Фамилия'),
                  'username': _('Имя пользователя'),
                  'password1': _('Пароль'),
                  'password2': _('Подтверждение пароля')}


class HexletLoginForm(AuthenticationForm):

    class Meta:
        model = HexletUser
        fields = ['username', 'password']


class HexletUserChangeForm(UserRegistrationForm):
    pass


class StatusCreationForm(ModelForm):
    name = forms.CharField(label=_('Имя'),
                           required=True,
                           widget=forms.TextInput(
                               attrs={'placeholder': _('Имя'),
                                      'class': 'form-control',
                                      'style':'max-width: 24em', }))
    class Meta:
        model = Statuses
        fields = ('name',)
        labels = {'name': _('Имя'),}


class StatusUpdateForm(StatusCreationForm):
    pass

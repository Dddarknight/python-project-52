from django import forms
from django.utils.translation import gettext as _
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from task_manager.models import HexletUser, Statuses, Tasks, Labels
from django.db.models import Q
import django_filters


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


class HexletUserChangeForm(UserRegistrationForm):
    pass


class StatusCreationForm(ModelForm):
    name = forms.CharField(label=_('Имя'),
                           required=True,
                           widget=forms.TextInput(
                               attrs={'placeholder': _('Имя'),
                                      'class': 'form-control',
                                      'style': 'max-width: 24em', }))

    class Meta:
        model = Statuses
        fields = ('name',)
        labels = {'name': _('Имя'), }


class StatusUpdateForm(StatusCreationForm):
    pass


class TaskCreationForm(ModelForm):
    name = forms.CharField(
        label=_('Имя'),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _('Имя'),
                                      'class': 'form-control',
                                      'style': 'width: 800px;', }))
    description = forms.CharField(
        label=_('Описание'),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _('Описание'),
                                      'class': 'form-control',
                                      'style': 'width: 800px;', }))
    status = forms.ModelChoiceField(
        label=_('Статус'),
        required=True,
        widget=forms.Select(
            attrs={'placeholder': _('Статус'),
                   'style': 'min-height: 50px; width: 800px;', }),
        queryset=Statuses.objects.all())
    executor = forms.ModelChoiceField(
        label=_('Исполнитель'),
        required=False,
        widget=forms.Select(
            attrs={'placeholder': _('Исполнитель'),
                   'style': 'min-height: 50px; width: 800px;', }),
        queryset=HexletUser.objects.exclude(Q(is_superuser=True)))
    label = forms.ModelMultipleChoiceField(
        label=_('Метки'),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'placeholder': _('Метки'),
                   'style': 'min-height: 50px; width: 800px;', }),
        queryset=Labels.objects.all())

    class Meta:
        model = Tasks
        fields = ('name', 'description', 'status', 'executor', 'label')


class TaskUpdateForm(TaskCreationForm):
    pass


class LabelCreationForm(ModelForm):
    name = forms.CharField(label=_('Имя'),
                           required=True,
                           widget=forms.TextInput(
                               attrs={'placeholder': _('Имя'),
                                      'class': 'form-control',
                                      'style': 'max-width: 24em', }))

    class Meta:
        model = Labels
        fields = ('name',)
        labels = {'name': _('Имя'), }


class LabelUpdateForm(LabelCreationForm):
    pass


def users_without_superuser(request):
    return HexletUser.objects.exclude(Q(is_superuser=True))


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label=_('Статус'), queryset=Statuses.objects.all())
    executor = django_filters.ModelChoiceFilter(
        label=_('Исполнитель'), queryset=users_without_superuser)
    label = django_filters.ModelChoiceFilter(
        label=_('Метка'), queryset=Labels.objects.all())
    only_executor = django_filters.BooleanFilter(field_name='executor',
                                                 label=_('Только свои задачи'),
                                                 widget=forms.CheckboxInput,
                                                 method='filter_executor')

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'label']

    def filter_executor(self, queryset, name, value):
        if value:
            return queryset.filter(executor_id=self.request.user.id)
        return queryset

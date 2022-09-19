from django import forms
from django.utils.translation import gettext as _
from django.forms import ModelForm
from task_manager.users.models import HexletUser
from task_manager.statuses.models import Statuses
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
from django.db.models import Q
import django_filters


def users_without_superuser(request):
    if HexletUser.objects.filter(is_superuser=True):
        return HexletUser.objects.exclude(Q(is_superuser=True))
    return HexletUser.objects.all()


class TaskCreationForm(ModelForm):
    name = forms.CharField(
        label=_('Имя'),
        label_suffix='',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _('Имя'),
                                      'class': 'form-control',
                                      'style': 'width: 800px;', }),
        error_messages={'unique': _(
            'Task с таким Имя уже существует')})
    description = forms.CharField(
        label=_('Описание'),
        label_suffix='',
        required=True,
        widget=forms.Textarea(attrs={'placeholder': _('Описание'),
                                     'class': 'form-control',
                                     'style': 'width: 800px;', }))
    status = forms.ModelChoiceField(
        label=_('Статус'),
        label_suffix='',
        required=True,
        widget=forms.Select(
            attrs={'placeholder': _('Статус'),
                   'style': 'min-height: 50px; width: 800px;', }),
        queryset=Statuses.objects.all())
    executor = forms.ModelChoiceField(
        label=_('Исполнитель'),
        label_suffix='',
        required=False,
        widget=forms.Select(
            attrs={'style': 'min-height: 50px; width: 800px;', }),
        queryset=HexletUser.objects.all())
    labels = forms.ModelMultipleChoiceField(
        label=_('Метки'),
        label_suffix='',
        required=False,
        widget=forms.SelectMultiple(
            attrs={'placeholder': _('Метки'),
                   'style': 'min-height: 50px; width: 800px;', }),
        queryset=Labels.objects.all())

    class Meta:
        model = Tasks
        fields = ('name', 'description', 'status', 'executor', 'labels')


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label=_('Статус'), label_suffix='', queryset=Statuses.objects.all())
    executor = django_filters.ModelChoiceFilter(
        label=_('Исполнитель'),
        label_suffix='',
        queryset=users_without_superuser)
    labels = django_filters.ModelChoiceFilter(
        label=_('Метка'), label_suffix='', queryset=Labels.objects.all())
    only_author = django_filters.BooleanFilter(field_name='author',
                                               label=_('Только свои задачи'),
                                               label_suffix='',
                                               widget=forms.CheckboxInput,
                                               method='filter_author')

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels']

    def filter_author(self, queryset, name, value):
        if value:
            return queryset.filter(author_id=self.request.user.id)
        return queryset

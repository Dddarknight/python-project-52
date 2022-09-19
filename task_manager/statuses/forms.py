from django import forms
from django.utils.translation import gettext as _
from django.forms import ModelForm
from task_manager.statuses.models import Statuses


class StatusCreationForm(ModelForm):
    name = forms.CharField(label=_('Имя'),
                           label_suffix='',
                           required=True,
                           widget=forms.TextInput(
                               attrs={'placeholder': _('Имя'),
                                      'class': 'form-control',
                                      'style': 'max-width: 24em', }),
                           error_messages={'unique': _(
                                'Task status с таким Имя уже существует')})

    class Meta:
        model = Statuses
        fields = ('name',)

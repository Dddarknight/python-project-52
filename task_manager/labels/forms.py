from django import forms
from django.utils.translation import gettext as _
from django.forms import ModelForm
from task_manager.labels.models import Labels


class LabelCreationForm(ModelForm):
    name = forms.CharField(label=_('Имя'),
                           label_suffix='',
                           required=True,
                           widget=forms.TextInput(
                               attrs={'placeholder': _('Имя'),
                                      'class': 'form-control',
                                      'style': 'max-width: 24em', }))

    class Meta:
        model = Labels
        fields = ('name',)


class LabelUpdateForm(LabelCreationForm):
    name = forms.CharField(label=_('Имя'),
                           label_suffix='',
                           initial='',
                           required=True,
                           widget=forms.TextInput(
                               attrs={'placeholder': _('Имя'),
                                      'class': 'form-control',
                                      'style': 'max-width: 24em', }))

    class Meta:
        model = Labels
        fields = ('name',)

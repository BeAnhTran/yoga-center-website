from django import forms
from django.utils.translation import ugettext_lazy as _


class FilterForm(forms.Form):
    BASIC_LEVEL = 0
    INTERMEDIATE_LEVEL = 1
    ADVANCED_LEVEL = 2
    LEVEL_CHOICES = (
        (None, 'Chọn cấp độ'),
        (BASIC_LEVEL, _('Basic Level')),
        (INTERMEDIATE_LEVEL, _('Intermediate Level')),
        (ADVANCED_LEVEL, _('Advanced Level')),
    )

    level = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'circle-select'}),
        choices=LEVEL_CHOICES,
        required=False)
    course = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': 'circle-select'}),
        required=False)
    trainer = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': 'circle-select'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('initial') is not None:
            if kwargs.get('initial').get('query_course') is not None:
                self.fields['course'].choices = kwargs['initial']['query_course']
            if kwargs.get('initial').get('query_trainer') is not None:
                self.fields['trainer'].choices = kwargs['initial']['query_trainer']

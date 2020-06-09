from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Field
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

import datetime
from django.utils import formats

from apps.cards.models import Card


class CardFormForTraineeEnroll(forms.ModelForm):
    start_at = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Please enter the value'),
                'class': 'form-control',
                'autoComplete': "off"
            },
        )
    )
    end_at = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Please enter the value'),
                'class': 'form-control',
                'autoComplete': "off"
            },
        )
    )
    lesson_list = forms.CharField(widget=forms.HiddenInput())
    payment_period = forms.ChoiceField(
        widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card_type'].empty_label = _('Please select a value')
        self.fields['start_at'].required = False
        self.fields['end_at'].required = False
        self.fields['payment_period'].required = False
        self.fields['lesson_list'].required = True
        if kwargs.get('initial') is not None:
            if kwargs.get('initial').get('card_type_list') is not None:
                self.fields['card_type'].queryset = kwargs['initial']['card_type_list']
            if kwargs.get('initial').get('payment_period_choices') is not None:
                self.fields['payment_period'].choices = kwargs['initial']['payment_period_choices']
        self.fields['card_type'].widget.attrs.update({
            'class': 'form-control'
        })
        self.helper = FormHelper()
        self.helper.form_id = 'form_enroll'

        # Focus on form field whenever error occurred
        errorList = list(self.errors)
        if errorList:
            for item in errorList:
                if item == '__all__':
                    break
                self.fields[item].widget.attrs.update(
                    {'autofocus': 'autofocus'})
                break
        else:
           self.fields['card_type'].widget.attrs.update(
               {'autofocus': 'autofocus'})

    class Meta:
        model = Card
        exclude = ['created_at', 'updated_at',
                   'yogaclass', 'trainee', 'lessons']

    def clean_end_at(self):
        cleaned_data = super(CardFormForTraineeEnroll, self).clean()
        end_at = cleaned_data['end_at']
        if 'start_at' in cleaned_data and end_at is not None:
            start_at = cleaned_data['start_at']
            if end_at < start_at:
                raise forms.ValidationError(
                    _('End at must be greater than Start at'))
        return end_at

    def clean(self):
        cleaned_data = super(CardFormForTraineeEnroll, self).clean()
        if 'start_at' in cleaned_data and 'end_at' in cleaned_data:
            start_at = cleaned_data['start_at']
            end_at = cleaned_data['end_at']
            if start_at is not None and end_at is not None:
                if self.initial.get('yoga_class') is not None:
                    yoga_class = self.initial.get('yoga_class')
                    lesson_list = yoga_class.lessons.filter(
                        date__range=[start_at, end_at], is_full=False)
                    if not lesson_list:
                        raise forms.ValidationError(
                            _('Your range time does not have any lessons'))
        return cleaned_data

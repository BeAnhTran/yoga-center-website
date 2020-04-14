from django import forms
from django.db import transaction
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from apps.lessons.models import Lesson
from apps.rooms.models import Room

from getenv import env

import datetime
from django.utils import formats

from apps.lectures.models import Lecture


class LessonForm(forms.ModelForm):
    trainer = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = datetime.datetime.now()
        range_time = env('DEFAULT_RANGE_TIME_MINUTES_OF_LESSON')
        now_with_range = now + datetime.timedelta(minutes=range_time)
        self.fields['room'].required = True
        self.fields['room'].label = _('room').capitalize()
        self.fields['date'] = forms.DateField(
            label=_('date').capitalize(),
            widget=DatePicker(options={
                'useCurrent': True,
            }, attrs={
                'placeholder': formats.date_format(now, use_l10n=True)
            }),
        )
        self.fields['start_time'] = forms.TimeField(
            label=_('start time').capitalize(),
            widget=TimePicker(options={
                'useCurrent': True,
                'format': 'HH:mm',
            }, attrs={
                'placeholder': now.strftime("%H:%M")
            }),
        )
        self.fields['end_time'] = forms.TimeField(
            label=_('end time').capitalize(),
            widget=TimePicker(options={
                'format': 'HH:mm',
            }, attrs={
                'placeholder': now_with_range.strftime("%H:%M")
            }),
        )
        self.fields['notes'].label = _('notes').capitalize()
        self.fields['notes'].widget.attrs = {
            'rows': 2,
            'columns': 10,
            'placeholder': _('notes')
        }
        self.fields['trainer'].label = _('trainer').capitalize()
        self.fields['trainer'].required = False
        self.fields['trainer'].widget.attrs['readonly'] = True

        self.fields['state'].label = _('state').capitalize()

        self.fields['lectures'].label = _('lectures').capitalize()
        self.fields['lectures'].widget = forms.CheckboxSelectMultiple()
        self.fields['lectures'].required = False

        if kwargs.get('initial') is not None:
            if kwargs.get('initial').get('lectures') is not None:
                self.fields['lectures'].choices = kwargs['initial']['lectures']
            
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'form_new_lesson'

        self.helper.layout = Layout(
            Row(
                Column('room', css_class='form-group col-md-6 mb-0'),
                Column('trainer', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_time', css_class='form-group col-md-6 mb-0'),
                Column('end_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('lectures', css_class='form-group col-md-6 mb-0'),
                Column('notes', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', _('Save'), css_class='btn-success'))

    class Meta:
        model = Lesson
        exclude = ['created_at', 'updated_at', 'cards']

    def clean_end_time(self):
        cleaned_data = self.cleaned_data
        end_time = cleaned_data['end_time']
        if 'start_time' in cleaned_data and end_time is not None:
            start_time = cleaned_data['start_time']
            if end_time < start_time:
                raise forms.ValidationError(
                    _('End time must be greater than start time'))
        return end_time

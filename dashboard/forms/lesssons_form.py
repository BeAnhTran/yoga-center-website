from django import forms
from django.db import transaction
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from lessons.models import Lesson
from rooms.models import Room

from getenv import env

import datetime
from django.utils import formats

from lessons.utils import check_overlap_in_list_lesson


class LessonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = datetime.datetime.now()
        range_time = env('DEFAULT_RANGE_TIME_MINUTES_OF_LESSON')
        now_with_range = now + datetime.timedelta(minutes=range_time)
        self.fields['room'].required = True
        self.fields['room'].label = _('room').capitalize()
        self.fields['day'] = forms.DateField(
            label=_('day').capitalize(),
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
        self.fields['content'].label = _('content').capitalize()
        self.fields['content'].widget.attrs = {
            'rows': 2,
            'columns': 10,
            'placeholder': _('content')
        }
        self.fields['trainer'].label = _('trainer').capitalize()
        self.fields['state'].label = _('state').capitalize()

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
                Column('day', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_time', css_class='form-group col-md-6 mb-0'),
                Column('end_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('content', css_class='form-group col-md-6 mb-0'),
                Column('notes', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', _('Save'), css_class='btn-success'))

    class Meta:
        model = Lesson
        exclude = ['created_at', 'updated_at']

    def clean_end_time(self):
        cleaned_data = self.cleaned_data
        end_time = cleaned_data['end_time']
        if 'start_time' in cleaned_data and end_time is not None:
            start_time = cleaned_data['start_time']
            if end_time < start_time:
                raise forms.ValidationError(
                    _('End time must be greater than start time'))
        return end_time

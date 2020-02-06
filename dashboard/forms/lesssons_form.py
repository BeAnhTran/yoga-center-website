from django import forms
from django.db import transaction
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from tempus_dominus.widgets import DatePicker, TimePicker
from lessons.models import Lesson


class LessonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['day'] = forms.DateField(
            widget=DatePicker(),
        )
        self.fields['start_time'] = forms.TimeField(
            widget=TimePicker(options={
                'disabledHours': [0, 1, 2, 3, 4, 23],
                'format': 'HH:mm'
            }),
        )
        self.fields['end_time'] = forms.TimeField(
            required=False,
            widget=TimePicker(options={
                'disabledHours': [0, 1, 2, 3, 4, 23],
                'format': 'HH:mm'
            }),
        )
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'form_new_lesson'
        self.fields['notes'].widget.attrs['rows'] = 2
        self.fields['notes'].widget.attrs['columns'] = 10
        self.helper.layout = Layout(
            'room',
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
            'notes',
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
                    _('error_end_time_must_be_greater_than_start_time'))
        return end_time

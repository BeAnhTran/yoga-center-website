from django import forms
from django.db import transaction
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from classes.models import YogaClass
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from datetime import datetime
from django.utils.formats import get_format


class ClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'placeholder': _('Name')})
        self.fields['description'].widget.attrs.update(
            {'placeholder': _('Description')})
        self.fields['start_at'] = forms.DateField(
            widget=DatePicker(
                options={
                    'useCurrent': True,
                },
                attrs={
                    'icon_toggle': True,
                    'input_group': False,
                }
            ),
        )
        self.fields['end_at'] = forms.DateField(
            required=False,
            widget=DatePicker(
                options={
                    'useCurrent': True,
                },
                attrs={
                    'icon_toggle': True,
                    'input_group': False,
                }
            ),
        )
        self.fields['end_at'].required = False
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', _('Save'), css_class='btn btn-success'))

        # Focus on form field whenever error occurred
        errorList = list(self.errors)
        if errorList:
            for item in errorList:
                self.fields[item].widget.attrs.update(
                    {'autofocus': 'autofocus'})
                break
        else:
            self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

    class Meta:
        model = YogaClass
        # localized_fields = ('start_at',)
        exclude = ['slug', 'created_at', 'updated_at']

    def clean_name(self):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError
        name = self.cleaned_data['name']
        slug = slugify(name)
        if YogaClass.objects.filter(slug=slug).exists():
            raise ValidationError(_('A class with this name already exists.'))

        return name

    def clean_end_at(self):
        cleaned_data = super(ClassForm, self).clean()
        end_at = cleaned_data['end_at']
        if 'start_at' in cleaned_data and end_at is not None:
            start_at = cleaned_data['start_at']
            if end_at < start_at:
                raise forms.ValidationError(
                    _('error_end_at_must_be_greater_than_start_at'))
        return end_at

class ClassNewForm(ClassForm):
    def clean_start_at(self):
        cleaned_data = super(ClassForm, self).clean()
        start_at = cleaned_data['start_at']
        if start_at < datetime.now().date():
            raise forms.ValidationError(_('wrong_start_date'))
        return start_at


class ClassEditForm(ClassForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if 'name' in self.changed_data:
            from django.utils.text import slugify
            from django.core.exceptions import ValidationError
            slug = slugify(name)
            if YogaClass.objects.filter(slug=slug).exists():
                raise ValidationError(
                    _('A class with this name already exists.'))
            return name
        else:
            return name

    def clean_start_at(self):
        return super(ClassForm, self).clean()['start_at']

from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from apps.classes.models import YogaClass
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from datetime import datetime
from django.utils.formats import get_format
from django.utils import formats
from apps.cards.models import CardType


class ClassForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'placeholder': 'Lớp CB 2-4-6'})
        self.fields['start_at'] = forms.DateField(
            label=_('start at').capitalize(),
            widget=DatePicker(
                options={
                    'useCurrent': True,
                },
                attrs={
                    'icon_toggle': True,
                    'input_group': False,
                    'placeholder': formats.date_format(datetime.now(), use_l10n=True)
                }
            ),
        )
        self.fields['end_at'] = forms.DateField(
            required=False,
            label=_('end at').capitalize(),
            widget=DatePicker(
                options={
                    'useCurrent': True,
                },
                attrs={
                    'icon_toggle': True,
                    'input_group': False,
                    'placeholder': formats.date_format(datetime.now(), use_l10n=True)
                }
            ),
        )
        self.fields['end_at'].required = False
        self.fields['price_per_lesson'].widget.attrs.update({
            'placeholder': '50.000'
        })
        self.fields['price_per_month'].widget.attrs.update({
            'placeholder': '600.000'
        })
        self.fields['price_for_training_class'].widget.attrs.update({
            'placeholder': '10.000.000'
        })
        self.fields['max_people'].widget.attrs.update({
            'placeholder': 25
        })
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'course',
            'name',
            Row(
                Column('trainer', css_class='form-group col-md-6 mb-0'),
                Column('max_people', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('price_per_lesson', css_class='form-group col-md-4 mb-0'),
                Column('price_per_month', css_class='form-group col-md-4 mb-0'),
                Column('price_for_training_class', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_at', css_class='form-group col-md-6 mb-0'),
                Column('end_at', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', _('Save'), css_class='btn-success'))

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
                    _('End at must be greater than Start at'))
        return end_at


class ClassNewForm(ClassForm):
    def clean_start_at(self):
        cleaned_data = super(ClassForm, self).clean()
        start_at = cleaned_data['start_at']
        if start_at < datetime.now().date():
            raise forms.ValidationError(_('wrong start date'))
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

from django import forms
from django.db import transaction
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from tempus_dominus.widgets import DatePicker, DateTimePicker
from getenv import env
import datetime
from django.utils import formats
from promotions.models import Promotion, PromotionType
from django.forms.models import inlineformset_factory
from dashboard.custom_layout_object import Formset


class PromotionTypeInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].widget.attrs.update(
            {'placeholder': _('value')}
        )

    class Meta:
        model = PromotionType
        exclude = ['created_at', 'updated_at']


PromotionTypeFormSet = inlineformset_factory(
    Promotion, PromotionType, form=PromotionTypeInlineForm,
    fields=['category', 'value'], extra=1, can_delete=True
)


class PromotionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['name'].widget.attrs.update(
            {'placeholder': _('promotion')}
        ),
        self.fields['start_at'] = forms.DateField(
            label=_('start time').capitalize(),
            widget=DatePicker(
                options={
                    'useCurrent': False,
                }, attrs={
                    'placeholder': formats.date_format(datetime.datetime.now(), use_l10n=True)
                }),
            required=False,
        )
        self.fields['end_at'] = forms.DateField(
            label=_('end time').capitalize(),
            widget=DatePicker(
                options={
                    'useCurrent': False,
                }, attrs={
                    'placeholder': formats.date_format(datetime.datetime.now(), use_l10n=True)
                }),
            required=False,
        )

        self.helper = FormHelper()
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            'name',
            'image',
            'description',
            Row(
                Column('start_at', css_class='form-group col-md-6 mb-0'),
                Column('end_at', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Fieldset(_('Promotion type'), Formset('promotion_types')),
            Submit('submit', _('Save'), css_class='btn-success'))

    class Meta:
        model = Promotion
        exclude = ['created_at', 'updated_at', 'slug']

    def clean_end_at(self):
        cleaned_data = self.cleaned_data
        end_at = cleaned_data['end_at']
        if 'start_at' in cleaned_data and end_at is not None:
            start_at = cleaned_data['start_at']
            if end_at < start_at:
                raise forms.ValidationError(
                    _('End at must be greater than start at'))
        return end_at


class PromotionEditForm(PromotionForm):
   def clean_name(self):
        name = self.cleaned_data['name']
        if 'name' in self.changed_data:
            from django.utils.text import slugify
            from django.core.exceptions import ValidationError
            slug = slugify(name)
            if Promotion.objects.filter(slug=slug).exists():
                raise ValidationError(
                    _('A promotion with this name already exists.'))
            return name
        else:
            return name

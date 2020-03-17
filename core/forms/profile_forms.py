from django import forms
from core.models import User, Trainee
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.helper import FormHelper
from django.utils.translation import gettext as _
from crispy_forms.bootstrap import InlineRadios
from tempus_dominus.widgets import DatePicker
from datetime import datetime
from django.utils import formats
from django.urls import reverse


class UsernameEmailForm(forms.ModelForm):
    hidden_field = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {
            'placeholder': 'greytran27@lotus.yoga.com'
        }
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'form_username_email'
        self.helper.form_class = 'col-md-9'
        self.helper.layout = Layout(
            'hidden_field',
            Row(
                Column('email'),
            ),
            Row(
                Column(
                    Submit('submit', _('Save'),
                           css_class='btn-success float-right'),
                )
            ))

    class Meta:
        model = User
        fields = ['email']


class BasicInfoForm(forms.ModelForm):
    hidden_field = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {
            'placeholder': 'Grey'
        }
        self.fields['last_name'].widget.attrs = {
            'placeholder': 'Tran'
        }
        self.fields['phone_number'].widget.attrs = {
            'placeholder': '(84) 989898'
        }
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'form_basic_info'
        self.fields['birth_day'] = forms.DateField(
            label=_('birth day').capitalize(),
            widget=DatePicker(
                attrs={
                    'icon_toggle': True,
                    'input_group': False,
                    'placeholder': formats.date_format(datetime.now(), use_l10n=True)
                }
            )
        )
        self.helper.layout = Layout(
            'hidden_field',
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column(
                    Field('gender', template="profile/custom_gender.html"), css_class="col-md-3"),
                Column('birth_day', css_class="col-md-3"),
                Column('phone_number', css_class="col-md-6"),
            ),
            Row(
                Column(
                    Submit('submit', _('Save'),
                           css_class='btn-success float-right'),
                )
            ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'gender', 'birth_day', 'phone_number']


class AdditionalInfoForm(forms.ModelForm):
    hidden_field = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs = {
            'placeholder': '140 A4 Street, Tan Binh Dict, Ho Chi Minh City'
        }

        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'form_additional_info'

        self.helper.layout = Layout(
            'hidden_field',
            Row(
                Column('address', css_class='col-md-6'),
                Column('country', css_class='col-md-3'),
                Column('language', css_class='col-md-3'),
            ),
            Row(
                Column(
                    Submit('submit', _('Save'),
                           css_class='btn-success float-right'),
                )
            ))

    class Meta:
        model = User
        fields = ['address', 'country', 'language']


class HealthConditionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['health_condition'].widget.attrs = {
            'placeholder': _('normal health')
        }
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'form_health_condition'

        self.helper.layout = Layout(
            'health_condition',
            Row(
                Column(
                    Submit('submit', _('Save'),
                           css_class='btn-success float-right'),
                )
            ))

    class Meta:
        model = Trainee
        fields = ['health_condition']

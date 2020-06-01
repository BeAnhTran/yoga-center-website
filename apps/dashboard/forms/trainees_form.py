from django import forms
from django.db import transaction
from allauth.account.forms import SignupForm
from apps.accounts.models import User, Trainee
from django_countries.fields import CountryField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.utils.translation import ugettext_lazy as _


class TraineeForm(SignupForm):
    first_name = forms.CharField(max_length=255, label=_('First name'), widget=forms.TextInput(
        attrs={'placeholder': _('First name')}))
    last_name = forms.CharField(max_length=255, label=_('Last name'), widget=forms.TextInput(
        attrs={'placeholder': _('Last name')}))
    phone_number = forms.CharField(max_length=255, label=_('Phone Number'), widget=forms.TextInput(
        attrs={'placeholder': '0932190999'}), required=False)
    country = CountryField().formfield(
        blank_label='(Select country)', initial='VN', label=_('Country'), required=False)
    health_condition = forms.CharField(
        widget=forms.Textarea, label=_('Health Condition'), required=False)
    health_condition.widget.attrs = {
        'rows': 4,
    }
    birth_day = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': 'cc'},
        ),
        label=_('Birth day'),
        required=False
    )
    gender = forms.ChoiceField(
        choices=User.GENDER_CHOICES, initial=User.GENDER_FEMALE, label=_('Gender'), required=False)
    address = forms.CharField(max_length=255, label=_('Address'), widget=forms.TextInput(
        attrs={'placeholder': _('Address')}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'autofocus': 'autofocus', 'placeholder': _('Email')})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-4 mb-0'),
                Column('birth_day', css_class='form-group col-md-4 mb-0'),
                Column('gender', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-6 mb-0'),
                Column('country', css_class='form-group col-md-6 mb-0'),
            ),
            'health_condition',
            Submit('submit', _('Save'))
        )

    @transaction.atomic
    def save(self, request):

        # Save the User instance and get a reference to it
        user = super(TraineeForm, self).save(request)
        # Create an instance of model with the extra fields
        # then save
        user.is_trainee = True
        user.phone_number = self.cleaned_data.get('phone_number')
        user.country = self.cleaned_data.get('country')
        user.birth_day = self.cleaned_data.get('birth_day')
        user.gender = self.cleaned_data.get('gender')
        user.address = self.cleaned_data.get('address')

        user.save()
        Trainee.objects.create(
            user=user, health_condition=self.cleaned_data.get('health_condition'))
        # You must return the original result.
        return user

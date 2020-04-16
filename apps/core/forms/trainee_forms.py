from django import forms
from django.db import transaction
from allauth.account.forms import SignupForm
from apps.accounts.models import User, Trainee
from django_countries.fields import CountryField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class TraineeSignupForm(SignupForm):
    first_name = forms.CharField(max_length=255, label='First Name', widget=forms.TextInput(
        attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=255, label='Last Name', widget=forms.TextInput(
        attrs={'placeholder': 'Last name'}))
    phone_number = forms.CharField(max_length=255, label='First Name', widget=forms.TextInput(
        attrs={'placeholder': '0905989898'}))
    country = CountryField().formfield(
        blank_label='(Select country)', initial='VN', required=False)
    health_condition = forms.CharField(widget=forms.Textarea, required=False)
    birth_day = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': 'cc'},
        )
    )
    gender = forms.ChoiceField(
        choices=User.GENDER_CHOICES, initial=User.GENDER_FEMALE)
    address = forms.CharField(max_length=255, label='Address', widget=forms.TextInput(
        attrs={'placeholder': 'Address'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
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
            Submit('submit', 'Sign up')
        )

    @transaction.atomic
    def save(self, request):

        # Save the User instance and get a reference to it
        user = super(TraineeSignupForm, self).save(request)
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

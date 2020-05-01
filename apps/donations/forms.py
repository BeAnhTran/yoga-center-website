from django import forms
from apps.donations.models import Donation
from django.utils.translation import ugettext_lazy as _


class DonationForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':  _('please input your name'),
                'class': 'input'
            }
        ))
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':  _('please input your email'),
                'class': 'input'
            }
        ))
    phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':  _('please input your phone'),
                'class': 'input'
            }
        ))
    content = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder':  _('please input content'),
            }
        )
    )
    amount = forms.FloatField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'class': 'input',
                'min': '1'
            })
    )

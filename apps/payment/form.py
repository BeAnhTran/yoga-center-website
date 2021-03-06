from django import forms
from django.utils.translation import ugettext_lazy as _


class CardPaymentForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':  _('please input your name'),
                'class': 'input',
                'autofocus': True
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
        required=False,
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder':  _('please input your phone'),
                'class': 'input'
            }
        ))


class PaymentForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':  _('please input your name'),
                'class': 'input',
                'autofocus': True
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
    address = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':  _('please input your address'),
                'class': 'input'
            }
        )
    )
    city = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':  _('please input your province/city'),
                'class': 'input'
            }
        )
    )

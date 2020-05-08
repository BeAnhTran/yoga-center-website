from django import forms
from django.utils.translation import ugettext_lazy as _


class SignUpFromHomeForm(forms.Form):
    email = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': _('Email')}))
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': _('First name')}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': _('Last name')}))
    phone_number = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': _('Phone number')}), required=False)
    health_condition = forms.CharField(
        widget=forms.Textarea, required=False)
    health_condition.widget.attrs = {
        'rows': 4,
        'placeholder': _('Health Condition')
    }

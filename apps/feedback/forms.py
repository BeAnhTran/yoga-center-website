from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from apps.feedback.models import Feedback


class FeedbackForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': _('Email')})
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': _('First name')})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': _('Last name')})
        self.fields['phone_number'].widget.attrs.update(
            {'placeholder': _('Phone number')})
        self.fields['content'].widget.attrs.update(
            {'placeholder': _('Content')})

    class Meta:
        model = Feedback
        exclude = ['created_at', 'updated_at']

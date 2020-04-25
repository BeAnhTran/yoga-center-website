from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from apps.feedback.models import Feedback


class FeedbackForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Feedback
        exclude = ['created_at', 'updated_at']

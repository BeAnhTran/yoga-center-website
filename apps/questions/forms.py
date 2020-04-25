from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from apps.questions.models import Question


class QuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': _('First name')})
        self.fields['first_name'].lable = ''
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': _('Last name')})
        self.fields['email'].widget.attrs.update(
            {'placeholder': _('Email')})
        self.fields['phone_number'].widget.attrs.update(
            {'placeholder': _('Phone number')})
        self.fields['content'].widget = forms.Textarea()
        self.fields['content'].widget.attrs.update(
            {'placeholder': _('Question')})

    class Meta:
        model = Question
        exclude = ['created_at', 'updated_at']

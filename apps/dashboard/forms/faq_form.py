from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from apps.faq.models import FAQ


class FAQForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update(
            {'placeholder': _('please input your question')})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'question',
            'answer',
            Submit('submit', _('Save'), css_class='btn-success'))

        # Focus on form field whenever error occurred
        errorList = list(self.errors)
        if errorList:
            for item in errorList:
                self.fields[item].widget.attrs.update(
                    {'autofocus': 'autofocus'})
                break
        else:
            self.fields['question'].widget.attrs.update(
                {'autofocus': 'autofocus'})

    class Meta:
        model = FAQ
        exclude = ['created_at', 'updated_at']

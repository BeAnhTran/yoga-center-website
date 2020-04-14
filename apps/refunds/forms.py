from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Field
from apps.refunds.models import Refund


class RefundForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].widget.attrs = {
            'rows': 4
        }
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'form_refund'
        self.fields['lessons'].label = _('lessons').capitalize()
        self.fields['lessons'].widget = forms.CheckboxSelectMultiple()

        self.fields['card'].label = ''

        if kwargs.get('initial') is not None:
            if kwargs.get('initial').get('registered_lessons') is not None:
                self.fields['lessons'].choices = kwargs['initial']['registered_lessons']

        self.helper.layout = Layout(
            Field('card', css_class='d-none'),
            'lessons',
            'amount',
            'reason',
            Submit('submit', _('Save'), css_class='btn-success'))

    class Meta:
        model = Refund
        exclude = ['created_at', 'updated_at', 'state']

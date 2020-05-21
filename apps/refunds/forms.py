from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Field
from apps.refunds.models import Refund


class RefundForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].widget.attrs = {
            'rows': 4,
        }
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'form_refund'
        self.fields['roll_calls'].label = _('lessons').capitalize()
        self.fields['roll_calls'].widget = forms.CheckboxSelectMultiple()

        self.fields['card'].label = ''
        self.fields['amount'].widget.attrs.update({'readonly': True})
        if kwargs.get('initial') is not None:
            if kwargs.get('initial').get('unstudied_lessons') is not None:
                self.fields['roll_calls'].choices = kwargs['initial']['unstudied_lessons']

                # Focus on form field whenever error occurred
        errorList = list(self.errors)
        if errorList:
            for item in errorList:
                if item == '__all__':
                    break
                self.fields[item].widget.attrs.update(
                    {'autofocus': 'autofocus'})
                break

        self.helper.layout = Layout(
            Field('card', css_class='d-none'),
            'roll_calls',
            'amount',
            'reason',
            Submit('submit', _('Save'), css_class='btn-success'))

    class Meta:
        model = Refund
        exclude = ['created_at', 'updated_at', 'state']

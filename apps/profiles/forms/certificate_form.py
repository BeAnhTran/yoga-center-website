from django import forms
from django.utils.translation import gettext as _
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.helper import FormHelper
from apps.accounts.models import Certificate


class CertificateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'placeholder': 'tên chứng nhận'
        }
        self.fields['description'].widget.attrs = {
            'placeholder': 'mô tả về chứng nhận'
        }
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'form_certificate'
        self.helper.layout = Layout(
            'name',
            'description',
            'image',
            Submit('submit', _('Save'), css_class='btn-success'),
        )

    class Meta:
        model = Certificate
        fields = ['name', 'description', 'image']

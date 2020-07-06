from django import forms
from django.utils.translation import gettext as _
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.helper import FormHelper
from apps.accounts.models import Trainer


class TrainerInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_id = 'trainer_info_form'
        self.helper.layout = Layout(
            'introduction',
            'experience',
            'achievements',
            Submit('submit', _('Save'), css_class='site-btn sb-gradient float-right mb-3'),
        )

    class Meta:
        model = Trainer
        fields = ['introduction', 'experience', 'achievements']

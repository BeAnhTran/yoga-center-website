from django import forms
from django.db import transaction
from apps.card_types.models import CardType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from django.utils.translation import ugettext_lazy as _


class CardTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['multiplier'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Row(
                Column('form_of_using', css_class='form-group col-md-4 mb-0'),
                Column('multiplier', css_class='form-group col-md-4 mb-0'),
                Column('for_longtime_trainee_only',
                       css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save', css_class='btn btn-success')
        )

    class Meta:
        model = CardType
        exclude = ['created_at', 'updated_at']

    def clean_name(self):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError
        name = self.cleaned_data['name']
        if CardType.objects.filter(name=name).exists():
            raise ValidationError(
                _('A card type with this name already exists.'))
        return name

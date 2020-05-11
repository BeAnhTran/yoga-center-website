from django import forms
from django.db import transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from django.utils.translation import ugettext_lazy as _
from apps.rooms.models import Room


class RoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'autofocus': 'autofocus', 'placeholder': _('room')})
        self.fields['location'].widget.attrs.update(
            {'placeholder': _('location')})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'location',
            'description',
            Row(
                Column('max_people', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', _('Save'), css_class='btn-success')
        )

    class Meta:
        model = Room
        exclude = ['created_at', 'updated_at']

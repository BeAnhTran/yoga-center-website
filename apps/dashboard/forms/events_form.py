from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from apps.events.models import Event
from tempus_dominus.widgets import DatePicker


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'placeholder': 'Sự kiện thiện nguyện'})
        self.fields['location'].widget.attrs.update(
            {'placeholder': 'Nơi diễn ra sự kiện'})
        self.fields['start_at'] = forms.DateField(
            label=_('start at').capitalize(),
            widget=DatePicker(options={
                'useCurrent': True,
            }),
        )
        self.fields['image'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'content',
            Row(
                Column('location', css_class='form-group col-md-6 mb-0'),
                Column('max_people', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_at', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', _('Save'), css_class='btn-success'))

        # Focus on form field whenever error occurred
        errorList = list(self.errors)
        if errorList:
            for item in errorList:
                self.fields[item].widget.attrs.update(
                    {'autofocus': 'autofocus'})
                break
        else:
            self.fields['name'].widget.attrs.update(
                {'autofocus': 'autofocus'})

    class Meta:
        model = Event
        exclude = ['slug', 'created_at', 'updated_at']

    def clean_name(self):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError
        name = self.cleaned_data['name']
        slug = slugify(name)
        if Event.objects.filter(slug=slug).exists():
            raise ValidationError(
                _('A event with this name already exists.'))

        return name

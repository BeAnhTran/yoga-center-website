from django import forms
from django.db import transaction
from courses.models import Course
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'autofocus': 'autofocus', 'placeholder': 'Name'})
        self.fields['description'].widget.attrs.update(
            {'placeholder': 'Description'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'course_type',
            'description',
            'image',
            Submit('submit', 'Save', css_class='btn btn-success')
        )

    class Meta:
        model = Course
        exclude = ['slug', 'created_at', 'updated_at']

    def clean_name(self):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError
        name = self.cleaned_data['name']
        slug = slugify(name)
        if Course.objects.filter(slug=slug).exists():
            raise ValidationError('A course with this name already exists.')

        return name

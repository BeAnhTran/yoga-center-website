from django import forms
from django.db import transaction
from courses.models import Course
from lectures.models import Lecture
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from cards.models import CardType
from django.utils.translation import ugettext_lazy as _
from ..forms.lectures_form import LectureInlineForm
from django.forms.models import inlineformset_factory
from dashboard.custom_layout_object import Formset


LectureFormSet = inlineformset_factory(
    Course, Lecture, form=LectureInlineForm,
    fields=['name', 'description'], extra=1, can_delete=True
)


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'autofocus': 'autofocus', 'placeholder': 'Yoga cơ bản'})
        self.fields['description'].widget.attrs.update(
            {'placeholder': 'Yoga cho người mới bắt đầu với động tác cơ bản'})
        self.fields['price_per_lesson'].widget.attrs.update({
            'placeholder': '50.000'
        })
        self.fields['price_per_month'].widget.attrs.update({
            'placeholder': '600.000'
        })
        self.fields['price_for_training_class'].widget.attrs.update({
            'placeholder': '10.000.000'
        })
        self.fields['card_types'] = forms.ModelMultipleChoiceField(label=_(
            'Card types'), widget=forms.CheckboxSelectMultiple(), queryset=CardType.objects.all())
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Row(
                Column('course_type', css_class='form-group col-md-4 mb-0'),
                Column('level', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'card_types',
            'content',
            'image',
            Row(
                Column('price_per_lesson', css_class='form-group col-md-4 mb-0'),
                Column('price_per_month', css_class='form-group col-md-4 mb-0'),
                Column('price_for_training_class',
                       css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Fieldset(_('Lectures'), Formset('lectures')),
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


class CourseEditForm(CourseForm):
   def clean_name(self):
        name = self.cleaned_data['name']
        if 'name' in self.changed_data:
            from django.utils.text import slugify
            from django.core.exceptions import ValidationError
            slug = slugify(name)
            if Course.objects.filter(slug=slug).exists():
                raise ValidationError(
                    _('A course with this name already exists.'))
            return name
        else:
            return name

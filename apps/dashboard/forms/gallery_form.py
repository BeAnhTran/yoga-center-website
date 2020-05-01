from django import forms
from django.db import transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from django.utils.translation import ugettext_lazy as _
from ..forms.gallery_image_form import GalleryImageInlineForm
from django.forms.models import inlineformset_factory
from apps.dashboard.custom_layout_object import Formset
from apps.gallery.models import GalleryImage, Gallery


GalleryImageFormSet = inlineformset_factory(
    Gallery, GalleryImage, form=GalleryImageInlineForm,
    fields=['image'], extra=1, can_delete=True
)


class GalleryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'placeholder': _('title')})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Fieldset(_('Images'), Formset('gallery_images')),
            Submit('submit', 'Save', css_class='btn btn-success')
        )
        self.helper.form_enctype = 'multipart/form-data'

    class Meta:
        model = Gallery
        exclude = ['slug', 'created_at', 'updated_at']

    def clean_title(self):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError
        title = self.cleaned_data['title']
        slug = slugify(title)
        if Gallery.objects.filter(slug=slug).exists():
            raise ValidationError('A gallery with this title already exists.')
        return title


class GalleryEditForm(GalleryForm):
   def clean_title(self):
        title = self.cleaned_data['title']
        if 'title' in self.changed_data:
            from django.utils.text import slugify
            from django.core.exceptions import ValidationError
            slug = slugify(title)
            if Gallery.objects.filter(slug=slug).exists():
                raise ValidationError(
                    _('A gallery with this title already exists.'))
            return title
        else:
            return title

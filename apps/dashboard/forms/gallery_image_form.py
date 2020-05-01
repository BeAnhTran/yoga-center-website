from django import forms
from apps.gallery.models import GalleryImage
from django.utils.translation import ugettext_lazy as _


class GalleryImageInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = GalleryImage
        exclude = ()

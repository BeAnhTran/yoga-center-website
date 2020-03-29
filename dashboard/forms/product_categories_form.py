from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from shop.models import ProductCategory


class ProductCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'placeholder': 'áo, quần,...'})

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'parent',
            Submit('submit', _('Save'), css_class='btn-success'))

        # Focus on form field whenever error occurred
        errorList = list(self.errors)
        if errorList:
            for item in errorList:
                self.fields[item].widget.attrs.update(
                    {'autofocus': 'autofocus'})
                break
        else:
            self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

    class Meta:
        model = ProductCategory
        exclude = ['slug', 'created_at', 'updated_at']

    def clean_name(self):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError
        name = self.cleaned_data['name']
        slug = slugify(name)
        if ProductCategory.objects.filter(slug=slug).exists():
            raise ValidationError(
                _('A product category with this name already exists.'))

        return name

from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from apps.shop.models import Product


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'placeholder': 'Áo thun'})
        self.fields['description'].widget.attrs.update(
            {'placeholder': 'Áo thun co giãn 4 chiều'})
        self.fields['price'].widget.attrs.update(
            {'placeholder': '200 000'})
        self.fields['promotion_price'].widget.attrs.update(
            {'placeholder': '100 000'})
        self.fields['quantity'].widget.attrs.update(
            {'placeholder': '20'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'category',
            Row(
                Column('image', css_class='form-group col-md-6 mb-0'),
                Column('quantity', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('price', css_class='form-group col-md-6 mb-0'),
                Column('promotion_price', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
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
        model = Product
        exclude = ['slug', 'created_at', 'updated_at']

    def clean_name(self):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError
        name = self.cleaned_data['name']
        slug = slugify(name)
        if Product.objects.filter(slug=slug).exists():
            raise ValidationError(
                _('A product with this name already exists.'))

        return name

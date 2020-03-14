from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from blog.models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'placeholder': 'Thêm yêu cuộc sống hơn'})
        self.fields['description'].widget.attrs.update(
            {'placeholder': 'Cuộc sống tốt đẹp hơn nếu ta biết thông cảm'})
        self.fields['content'].widget.attrs.update(
            {'placeholder': 'Mô tả nội dung chi tiết'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'category',
            Row(
                Column('image', css_class='form-group col-md-6 mb-0'),
                Column('status', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            'content',
            Submit('submit', _('Save'), css_class='btn-success'))

        # Focus on form field whenever error occurred
        errorList = list(self.errors)
        if errorList:
            for item in errorList:
                self.fields[item].widget.attrs.update(
                    {'autofocus': 'autofocus'})
                break
        else:
            self.fields['title'].widget.attrs.update(
                {'autofocus': 'autofocus'})

    class Meta:
        model = Post
        exclude = ['slug', 'created_at', 'updated_at']

    def clean_title(self):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError
        title = self.cleaned_data['title']
        slug = slugify(title)
        if Post.objects.filter(slug=slug).exists():
            raise ValidationError(
                _('A post with this name already exists.'))

        return title

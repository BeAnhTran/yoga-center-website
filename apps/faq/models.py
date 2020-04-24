from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _


class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name=_('question'))
    answer = RichTextUploadingField(verbose_name=_('answer'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

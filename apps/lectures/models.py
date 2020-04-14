from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from apps.courses.models import Course
from apps.common.templatetags import sexify
from ckeditor_uploader.fields import RichTextUploadingField


class Lecture(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='lectures', verbose_name=_('course'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('description'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.name

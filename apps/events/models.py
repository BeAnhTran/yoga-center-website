from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Event(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('name'))
    slug = models.SlugField(max_length=250, unique=True,
                            verbose_name=_('slug'))
    image = models.ImageField(
        upload_to='events/', null=True, verbose_name=_('image'))
    content = RichTextUploadingField(verbose_name=_('content'))
    max_people = models.IntegerField(
        blank=True, null=True, verbose_name=_('max people'))
    location = models.CharField(max_length=255, verbose_name=_('location'))
    start_at = models.DateField(verbose_name=_('start at'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

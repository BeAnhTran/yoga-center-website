from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify


class Gallery(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Gallery, self).save(*args, **kwargs)


class GalleryImage(models.Model):
    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='gallery', blank=True, null=True, verbose_name=_('image'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

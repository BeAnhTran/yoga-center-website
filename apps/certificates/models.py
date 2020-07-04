from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.courses.models import Course

# Create your models here.


class Certificate(models.Model):
    course = models.ForeignKey(
        Course, blank=True, null=True, on_delete=models.CASCADE, related_name='certificates', verbose_name=_('course'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.CharField(
        blank=True, null=True, max_length=255, verbose_name=_('description'))
    image = models.ImageField(upload_to='certificates',
                              blank=True, null=True, verbose_name=_('image'))

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.name

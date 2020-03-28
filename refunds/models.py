from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

from cards.models import Card
from lessons.models import Lesson

STATE_CHOICES = (
    ('pending', 'Pending'),
    ('approve', 'Approve'),
    ('reject', 'Reject'),
)


class Refund(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='refunds', verbose_name=_('card')
    )
    lessons = models.ManyToManyField(
        Lesson, related_name='refunds', verbose_name=_('lessons'))
    amount = models.FloatField(verbose_name=_('amount'))
    reason = RichTextUploadingField(verbose_name=_('reason'))
    state = models.CharField(max_length=20,
                             choices=STATE_CHOICES,
                             default='pending')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

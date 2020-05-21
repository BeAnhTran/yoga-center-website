from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

from apps.cards.models import Card
from apps.roll_calls.models import RollCall

PENDING_STATE = 0
APPROVED_STATE = 1
REJECTED_STATE = 2

STATE_CHOICES = (
    (PENDING_STATE, _('pending')),
    (APPROVED_STATE, _('approved')),
    (REJECTED_STATE, _('rejected')),
)


class Refund(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='refunds', verbose_name=_('card'))
    roll_calls = models.ManyToManyField(
        RollCall, related_name='refunds', verbose_name=_('lessons'))
    amount = models.FloatField(verbose_name=_('amount'))
    reason = RichTextUploadingField(verbose_name=_('reason'))
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=PENDING_STATE, verbose_name=_('state'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

from django.db import models
from django.utils.translation import ugettext_lazy as _

from classes.models import YogaClass
from cards.models import Card
from promotions.models import ApplyPromotionCode
from django.contrib.contenttypes.fields import GenericRelation


class CardInvoice(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='card_invoices', verbose_name=_('card'))
    description = models.TextField(
        null=True, blank=True, verbose_name=_('description'))
    amount = models.FloatField(
        blank=True, null=True, verbose_name=_('amount'))
    charge_id = models.CharField(max_length=256, verbose_name=_(
        'charge id'), null=True, blank=True)
    apply_promotion_codes = GenericRelation(
        ApplyPromotionCode, related_query_name='card_invoices')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

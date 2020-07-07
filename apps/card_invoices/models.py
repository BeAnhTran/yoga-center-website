from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.classes.models import YogaClass, PaymentPeriod
from apps.cards.models import Card
from apps.promotions.models import ApplyPromotionCode
from django.contrib.contenttypes.fields import GenericRelation
from apps.accounts.models import Staff
from datetime import date, datetime, timedelta

PREPAID = 0
POSTPAID = 1
NOT_SPECIFIED = 2

PAYMENT_TYPES = (
    (PREPAID, _('Prepaid')),
    (POSTPAID, _('Postpaid')),
    (NOT_SPECIFIED, _('Not specified')),
)


class CardInvoice(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='invoices', verbose_name=_('card'))
    payment_period = models.ForeignKey(
        PaymentPeriod, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices', verbose_name=_('payment period'))
    description = models.TextField(
        null=True, blank=True, verbose_name=_('description'))
    amount = models.FloatField(
        blank=True, null=True, verbose_name=_('amount'))
    charge_id = models.CharField(max_length=256, verbose_name=_(
        'charge id'), null=True, blank=True)
    apply_promotion_codes = GenericRelation(
        ApplyPromotionCode, related_query_name='card_invoices')
    payment_type = models.IntegerField(
        choices=PAYMENT_TYPES, default=PREPAID, verbose_name=_('payment type'))
    staff = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, related_name='card_invoices', verbose_name=_('staff'), blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def is_charged(self):
        if self.payment_type == PREPAID and self.amount == 0:
            return True
        if self.charge_id or self.staff is not None:
            return True
        return False

    def get_expire_time(self):
        if self.is_charged() is False:
            if self.payment_type == POSTPAID:
                return self.created_at + timedelta(days=7)
            elif self.payment_type == NOT_SPECIFIED:
                return self.payment_period.end_at
        return None

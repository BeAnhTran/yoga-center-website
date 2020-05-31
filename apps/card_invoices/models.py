from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.classes.models import YogaClass
from apps.cards.models import Card
from apps.promotions.models import ApplyPromotionCode
from django.contrib.contenttypes.fields import GenericRelation

PREPAID = 0
POSTPAID = 1

PAYMENT_TYPES = (
    (PREPAID, _('Prepaid')),
    (POSTPAID, _('Postpaid')),
)


class CardInvoice(models.Model):
    card = models.OneToOneField(
        Card, on_delete=models.CASCADE, primary_key=True, related_name='invoice', verbose_name=_('card'))
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
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def is_charged(self):
        if self.amount == 0:
            return True
        if self.charge_id or self.check_staff():
            return True
        return False

    def check_staff(self):
        try:
            self.staff
            return True
        except:
            return False

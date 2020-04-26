from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.classes.models import YogaClass
from apps.cards.models import Card
from apps.promotions.models import ApplyPromotionCode
from django.contrib.contenttypes.fields import GenericRelation


class Donation(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    email = models.EmailField(max_length=255, verbose_name=_('email'))
    phone_number = models.CharField(
        max_length=25, blank=True, null=True, verbose_name=_('phone number'))
    content = models.CharField(max_length=255, verbose_name=_('content'))
    amount = models.FloatField(
        blank=True, null=True, verbose_name=_('amount'))
    charge_id = models.CharField(max_length=256, verbose_name=_(
        'charge id'), null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

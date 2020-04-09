from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from core.models import User


class Promotion(models.Model):
    name = models.CharField(max_length=225, verbose_name=_('name'))
    slug = models.SlugField(max_length=255, unique=True)
    description = RichTextUploadingField(verbose_name=_('description'))
    image = models.ImageField(
        upload_to='promotions/', null=True, verbose_name=_('image'))
    start_at = models.DateTimeField(
        verbose_name=_('start at'), null=True, blank=True)
    end_at = models.DateTimeField(
        verbose_name=_('end at'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Promotion, self).save(*args, **kwargs)


CASH_PROMOTION = 0
PLUS_TIME_PRACTICE_PROMOTION = 1
GIFT_PROMOTION = 2
PERCENT_PROMOTION = 3


CATEGORY_CHOICES = (
    (CASH_PROMOTION, _('Cash promotion')),
    (PLUS_TIME_PRACTICE_PROMOTION, _('Plus time practice promotion')),
    (GIFT_PROMOTION, _('Gift promotion')),
    (PERCENT_PROMOTION, _('Percent promotion')),
)

MONEY_UNIT = 0
LESSON_UNIT = 1
WEEK_PRACTICE_UNIT = 2
MONTH_PRACTICE_UNIT = 3
PRODUCT_UNIT = 4
PERCENT_UNIT = 5


UNIT_CHOICES = (
    (MONEY_UNIT, _('Money Unit')),
    (LESSON_UNIT, _('Lesson Unit')),
    (WEEK_PRACTICE_UNIT, _('Week practice unit')),
    (MONTH_PRACTICE_UNIT, _('Month practice unit')),
    (PRODUCT_UNIT, _('Product unit')),
    (PERCENT_UNIT, _('Percent unit')),
)


class PromotionType(models.Model):
    promotion = models.ForeignKey(
        Promotion, on_delete=models.CASCADE, related_name='promotion_types', verbose_name=_('promotion'))
    category = models.IntegerField(
        choices=CATEGORY_CHOICES, verbose_name=_('category'))
    amount = models.FloatField(verbose_name=_('amount'))
    unit = models.IntegerField(choices=UNIT_CHOICES, verbose_name=_('unit'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

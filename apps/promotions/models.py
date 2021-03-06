from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from apps.accounts.models import User
import uuid
from apps.common.templatetags import sexify
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.shop.models import Product


class Promotion(models.Model):
    name = models.CharField(max_length=225, verbose_name=_('name'))
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(
        max_length=255, verbose_name=_('description'))
    content = RichTextUploadingField(
        null=True, blank=True, verbose_name=_('content'))
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
PERCENT_PROMOTION = 1
FREE_SOME_LESSON_PROMOTION = 2
PLUS_MONTH_PRACTICE_PROMOTION = 3
GIFT_PROMOTION = 4


CATEGORY_CHOICES = (
    (CASH_PROMOTION, _('Cash promotion')),
    (PERCENT_PROMOTION, _('Percent promotion')),
    (FREE_SOME_LESSON_PROMOTION, _('Free some lesson promotion')),
    (PLUS_MONTH_PRACTICE_PROMOTION, _('Plus month practice promotion')),
    (GIFT_PROMOTION, _('Gift promotion')),
)


class PromotionType(models.Model):
    promotion = models.ForeignKey(
        Promotion, on_delete=models.CASCADE, related_name='promotion_types', verbose_name=_('promotion'))
    category = models.IntegerField(
        choices=CATEGORY_CHOICES, verbose_name=_('category'))
    value = models.FloatField(verbose_name=_('value or quantity'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('promotion', 'category'),)

    @property
    def full_title(self):
        if self.category == CASH_PROMOTION:
            return 'Khuyến mãi giảm ' + str(sexify.sexy_number(self.value)) + 'đ'
        elif self.category == FREE_SOME_LESSON_PROMOTION:
            return 'Khuyến mãi tặng tiền miễn phí ' + str(sexify.sexy_number(self.value)) + ' buổi tập'
        elif self.category == PLUS_MONTH_PRACTICE_PROMOTION:
            return 'Khuyến mãi tặng thêm ' + str(sexify.sexy_number(self.value)) + ' tháng tập'
        elif self.category == GIFT_PROMOTION:
            pos = -1
            s = 'Khuyến mãi tặng sản phẩm: '
            promotion_type_products = self.promotion_type_products.all()
            for p in promotion_type_products:
                pos += 1
                if pos == len(promotion_type_products) - 1:
                    s += str(p.quantity) + ' ' + p.product.name + '.'
                else:
                    s += str(p.quantity) + ' ' + p.product.name + ', '
            return s
        else:
            return 'Khuyến mãi giảm ' + str(sexify.sexy_number(self.value)) + '%'


# NOTE: PromotionTypeProduct: Product that is used for PromotionType with quantity


class PromotionTypeProduct(models.Model):
    promotion_type = models.ForeignKey(
        PromotionType, on_delete=models.CASCADE, related_name='promotion_type_products')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='promotion_type_products')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PromotionCode(models.Model):
    promotion = models.ForeignKey(
        Promotion, on_delete=models.CASCADE, related_name='codes', verbose_name=_('promotion'))
    promotion_type = models.ForeignKey(
        PromotionType, on_delete=models.CASCADE, null=True, related_name='codes', verbose_name=_('promotion type'))
    value = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# NOTE: Apply protion code for CardInvoice or (Product)Bill


class ApplyPromotionCode(models.Model):
    promotion_code = models.OneToOneField(
        PromotionCode, on_delete=models.CASCADE, primary_key=True, related_name='apply')
    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('content_type', 'object_id')

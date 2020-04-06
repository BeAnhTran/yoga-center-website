from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from core.models import User


class Product(models.Model):
    category = models.ForeignKey(
        'shop.ProductCategory', on_delete=models.CASCADE, verbose_name=_('category'))
    name = models.CharField(max_length=150, verbose_name=_('name'))
    slug = models.SlugField(max_length=175, unique=True)
    description = RichTextUploadingField(verbose_name=_('description'))
    image = models.ImageField(
        upload_to='products/', null=True, verbose_name=_('image'))
    price = models.FloatField(verbose_name=_('price'))
    promotion_price = models.FloatField(
        null=True, blank=True, verbose_name=_('promotion price'))
    quantity = models.IntegerField(verbose_name=_('quantity'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class ProductCategory(models.Model):
    name = models.CharField(max_length=150, unique=True,
                            verbose_name=_('name'))
    slug = models.SlugField(max_length=175, unique=True,
                            verbose_name=_('slug'))
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name='children', on_delete=models.CASCADE, verbose_name=_('parent category'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)


class Bill(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bills', verbose_name=_('user'))
    products = models.ManyToManyField(Product, through='ProductBill')
    description = models.TextField(
        null=True, blank=True, verbose_name=_('description'))
    amount = models.FloatField(
        blank=True, null=True, verbose_name=_('amount'))
    charge_id = models.CharField(max_length=255, verbose_name=_(
        'charge id'), null=True, blank=True)
    shipping_address = models.CharField(max_length=255, verbose_name=_(
        'shipping address'), null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))


class ProductBill(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


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


class Cart(models.Model):
    products = models.ManyToManyField(Product, through='ProductCart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

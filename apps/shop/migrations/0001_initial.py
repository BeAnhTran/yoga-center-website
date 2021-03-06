# Generated by Django 3.0.2 on 2020-07-04 02:13

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('amount', models.FloatField(blank=True, null=True, verbose_name='amount')),
                ('charge_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='charge id')),
                ('shipping_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='shipping address')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('slug', models.SlugField(max_length=175, unique=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='description')),
                ('image', models.ImageField(null=True, upload_to='products/', verbose_name='image')),
                ('price', models.FloatField(verbose_name='price')),
                ('promotion_price', models.FloatField(blank=True, null=True, verbose_name='promotion price')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=175, unique=True, verbose_name='slug')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.ProductCategory', verbose_name='parent category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Bill')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ProductCategory', verbose_name='category'),
        ),
        migrations.AddField(
            model_name='bill',
            name='products',
            field=models.ManyToManyField(through='shop.ProductBill', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='bill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]

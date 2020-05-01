# Generated by Django 3.0.2 on 2020-04-20 03:22

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('card_types', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='name')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='slug')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='content')),
                ('image', models.ImageField(blank=True, null=True, upload_to='course', verbose_name='image')),
                ('course_type', models.IntegerField(choices=[(0, 'Practice Course'), (1, 'Training Course')], default=0, verbose_name='course type')),
                ('level', models.IntegerField(choices=[(0, 'Basic Level'), (1, 'Intermediate Level'), (2, 'Advanced Level')], null=True, verbose_name='level')),
                ('price_per_lesson', models.FloatField(blank=True, null=True, verbose_name='price per lesson')),
                ('price_per_month', models.FloatField(blank=True, null=True, verbose_name='price per month')),
                ('price_for_training_class', models.FloatField(blank=True, null=True, verbose_name='price for training class')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
                ('card_types', models.ManyToManyField(related_name='courses', to='card_types.CardType', verbose_name='card types')),
            ],
        ),
    ]

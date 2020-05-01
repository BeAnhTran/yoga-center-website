# Generated by Django 3.0.2 on 2020-04-24 14:16

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='answer'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.CharField(max_length=255, verbose_name='question'),
        ),
    ]
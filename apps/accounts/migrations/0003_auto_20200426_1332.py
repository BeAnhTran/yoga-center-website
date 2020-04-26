# Generated by Django 3.0.2 on 2020-04-26 06:32

import ckeditor.fields
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_trainer_taught_lessons'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='achievements',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='sample achievement', verbose_name='achievements'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainer',
            name='introduction',
            field=models.TextField(default='sample introduction', verbose_name='introduction'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staff',
            name='experience',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='experience'),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='experience',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='experience'),
        ),
    ]

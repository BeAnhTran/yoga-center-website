# Generated by Django 3.0.2 on 2020-04-16 08:04

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0001_initial'),
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='amount')),
                ('reason', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='reason')),
                ('state', models.IntegerField(choices=[(0, 'pending'), (1, 'approved'), (2, 'rejected')], default=0, verbose_name='state')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refunds', to='cards.Card', verbose_name='card')),
                ('lessons', models.ManyToManyField(related_name='refunds', to='lessons.Lesson', verbose_name='lessons')),
            ],
        ),
    ]
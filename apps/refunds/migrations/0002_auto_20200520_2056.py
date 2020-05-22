# Generated by Django 3.0.2 on 2020-05-20 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roll_calls', '0001_initial'),
        ('refunds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refund',
            name='lessons',
        ),
        migrations.AddField(
            model_name='refund',
            name='roll_calls',
            field=models.ManyToManyField(related_name='refunds', to='roll_calls.RollCall', verbose_name='lessons'),
        ),
    ]
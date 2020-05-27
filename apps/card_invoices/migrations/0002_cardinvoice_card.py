# Generated by Django 3.0.2 on 2020-05-27 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0001_initial'),
        ('card_invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardinvoice',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_invoices', to='cards.Card', verbose_name='card'),
        ),
    ]

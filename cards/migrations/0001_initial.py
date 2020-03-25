# Generated by Django 3.0.2 on 2020-03-25 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('card_types', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
                ('card_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='card_types.CardType', verbose_name='card type')),
            ],
        ),
    ]

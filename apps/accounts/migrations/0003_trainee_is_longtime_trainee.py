# Generated by Django 3.0.2 on 2020-07-27 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_trainer_taught_lessons'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainee',
            name='is_longtime_trainee',
            field=models.BooleanField(default=False, verbose_name='is longtime trainee'),
        ),
    ]

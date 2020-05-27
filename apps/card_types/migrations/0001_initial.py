# Generated by Django 3.0.2 on 2020-05-27 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('form_of_using', models.IntegerField(choices=[(0, 'Full Month'), (1, 'For Some Lessons'), (2, 'Trial'), (3, 'For Training Course')], default=0, verbose_name='form of using')),
                ('min_lessons_require', models.IntegerField(blank=True, null=True, verbose_name='min lessons required')),
                ('multiplier', models.FloatField(null=True, verbose_name='multiplier')),
                ('for_longtime_trainee_only', models.BooleanField(default=False, verbose_name='for longtime trainee only')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
            ],
        ),
    ]

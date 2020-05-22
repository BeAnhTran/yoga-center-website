# Generated by Django 3.0.2 on 2020-05-22 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='name')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='location')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('max_people', models.IntegerField(verbose_name='max people')),
                ('state', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=0, verbose_name='state')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
            ],
        ),
    ]

# Generated by Django 3.0.2 on 2020-02-13 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('cards', '0002_card_trainee'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YogaClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='name')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='slug')),
                ('description', models.TextField(verbose_name='description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='class', verbose_name='image')),
                ('state', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1, verbose_name='state')),
                ('level', models.IntegerField(choices=[(0, 'Basic Level'), (1, 'Intermediate Level'), (2, 'Advanced Level')], default=0, verbose_name='level')),
                ('price_per_lesson', models.FloatField(blank=True, null=True, verbose_name='price_per_lesson')),
                ('price_per_month', models.FloatField(blank=True, null=True, verbose_name='price_per_month')),
                ('price_course', models.FloatField(blank=True, null=True, verbose_name='price_course')),
                ('max_people', models.IntegerField(blank=True, null=True, verbose_name='max_people')),
                ('start_at', models.DateField(blank=True, null=True, verbose_name='start_at')),
                ('end_at', models.DateField(blank=True, null=True, verbose_name='end_at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated_at')),
                ('card_types', models.ManyToManyField(related_name='classes', to='cards.CardType', verbose_name='card types')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='courses.Course', verbose_name='course')),
                ('form_trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classes', to='core.Trainer', verbose_name='form_trainer')),
            ],
            options={
                'verbose_name': 'Yoga Class',
                'verbose_name_plural': 'Yoga Classes',
                'ordering': ('created_at', 'name'),
            },
        ),
    ]

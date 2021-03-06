# Generated by Django 3.0.2 on 2020-07-04 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='certificates', verbose_name='image')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('yoga_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='classes.YogaClass', verbose_name='class')),
            ],
        ),
    ]

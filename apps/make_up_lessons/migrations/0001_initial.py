# Generated by Django 3.0.2 on 2020-05-22 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lessons', '0001_initial'),
        ('roll_calls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MakeUpLesson',
            fields=[
                ('roll_call', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='make_up_lesson', serialize=False, to='roll_calls.RollCall')),
                ('is_studied', models.BooleanField(default=False, verbose_name='studied')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated at')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='make_up_lessons', to='lessons.Lesson', verbose_name='lesson')),
            ],
        ),
    ]

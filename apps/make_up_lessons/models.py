from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.roll_calls.models import RollCall
from apps.lessons.models import Lesson
from django.db.models.signals import post_save
from django.dispatch import receiver


class MakeUpLesson(models.Model):
    roll_call = models.OneToOneField(
        RollCall, on_delete=models.CASCADE, primary_key=True, related_name='make_up_lesson')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='make_up_lessons', verbose_name='lesson')
    is_studied = models.BooleanField(default=False, verbose_name=_('studied'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))


@receiver(post_save, sender=MakeUpLesson)
def make_up_changed(sender, instance, **kwargs):
    lesson = instance.lesson
    if lesson.check_is_full():
        lesson.is_full = True
        lesson.save()

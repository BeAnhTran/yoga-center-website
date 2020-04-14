from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.cards.models import Card
from apps.lessons.models import Lesson
from django.db.models.signals import post_save
from django.dispatch import receiver


class RollCall(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='roll_calls', verbose_name=_('card'))
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='roll_calls', verbose_name=_('lesson'))
    studied = models.BooleanField(
        default=False, verbose_name=_('studied'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))


@receiver(post_save, sender=RollCall)
def cards_changed(sender, instance, **kwargs):
    lesson = instance.lesson
    if lesson.check_is_full():
        lesson.is_full = True
        lesson.save()

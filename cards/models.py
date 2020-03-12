from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Trainee
from classes.models import YogaClass
from card_types.models import CardType


class Card(models.Model):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='cards', verbose_name=_('trainee'))
    card_type = models.ForeignKey(
        CardType, on_delete=models.CASCADE, related_name='cards', verbose_name=_('card type'))
    yogaclass = models.ForeignKey(
        YogaClass, on_delete=models.CASCADE, related_name='cards', verbose_name=_('yoga class'))
    lessons = models.ManyToManyField(
        to='lessons.Lesson', through='roll_calls.RollCall', related_name='cards', verbose_name=_('lessons'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def end_at(self):
        return self.lessons.last().day

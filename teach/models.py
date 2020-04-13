from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Trainer
from lessons.models import Lesson
from django.db.models.signals import post_save
from django.dispatch import receiver


TAUGHT_STATE = 0
TAUGHT_INSTEAD_STATE = 1

STATE_CHOICES = (
    (TAUGHT_STATE, _('Taught')),
    (TAUGHT_INSTEAD_STATE, _('Taught Instead')),
)


class TrainerLesson(models.Model):
    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name='taught', verbose_name=_('trainer'))
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='taught', verbose_name=_('lesson'))
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=TAUGHT_STATE, verbose_name=_('state'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

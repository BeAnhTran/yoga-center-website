from django.db import models
from django.utils.translation import ugettext_lazy as _
from classes.models import YogaClass
from rooms.models import Room
from core.models import Trainer
import time

ACTIVE_STATE = 0
INACTIVE_STATE = 1

STATE_CHOICES = (
    (ACTIVE_STATE, _('Active')),
    (INACTIVE_STATE, _('Inactive')),
)


class Lesson(models.Model):
    yogaclass = models.ForeignKey(
        YogaClass, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('yogaclass'))
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, related_name='lessons', verbose_name=_('room'), blank=True, null=True)
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, related_name='lessons', verbose_name=_('trainer'), blank=True, null=True)
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=ACTIVE_STATE, verbose_name=_('state'))
    day = models.DateField(help_text=_(
        'Day of the event'), verbose_name=_('day'))
    start_time = models.TimeField(help_text=_(
        'Starting time'), verbose_name=_('start_time'))
    end_time = models.TimeField(help_text=_(
        'Final time'), verbose_name=_('end_time'))
    notes = models.TextField(help_text=_(
        'Notes'), blank=True, null=True, verbose_name=_('notes'))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('end_at'))

    def __str__(self):
        if self.room:
            return self.yogaclass.name + '-' + self.room.name + '-' + self.start_time.strftime('%H:%M')
        return self.yogaclass.name + '-' + self.start_time.strftime('%H:%M')

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.trainer:
                self.trainer = self.yogaclass.form_trainer
        
        super(Lesson, self).save(*args, **kwargs)
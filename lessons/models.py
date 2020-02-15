from django.db import models
from django.utils.translation import ugettext_lazy as _
from classes.models import YogaClass
from rooms.models import Room
from core.models import Trainer
import time
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from lessons.utils import check_overlap_in_list_lesson
from django.db.models import Q


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
    content = models.TextField(help_text=_(
        'Content'), blank=True, null=True, verbose_name=_('content'))
    notes = models.TextField(help_text=_(
        'Notes'), blank=True, null=True, verbose_name=_('notes'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('end_at'))

    def __str__(self):
        if self.room:
            return self.yogaclass.name + ' - ' + self.room.name + ' (' + self.start_time.strftime('%H:%M') + ' - ' + self.end_time.strftime('%H:%M') + ')'
        return self.yogaclass.name + ' - ' + self.start_time.strftime('%H:%M')

    def clean(self):
        room = self.room
        if self.id:
            class_lessons_on_day = self.yogaclass.lessons.filter(
                day=self.day).exclude(pk=self.id)
            room_lessons_on_day = room.lessons.filter(
                day=self.day).exclude(pk=self.id)
        else:
            class_lessons_on_day = self.yogaclass.lessons.filter(day=self.day)
            room_lessons_on_day = room.lessons.filter(day=self.day)
        check1 = check_overlap_in_list_lesson(
            self.start_time, self.end_time, class_lessons_on_day)
        check2 = check_overlap_in_list_lesson(
            self.start_time, self.end_time, room_lessons_on_day)
        if any(v['value'] is False for v in [check1, check2]):
            if check1['value'] is False:
                obj = check1['object']
            else:
                if check2['value'] is False:
                    obj = check2['object']
            raise ValidationError(_('overlap_time').capitalize() + ': ' + obj.__str__())

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.id:
            if not self.trainer:
                self.trainer = self.yogaclass.form_trainer

        super(Lesson, self).save(*args, **kwargs)

from datetime import date
from django.db import models
from django.utils.translation import ugettext_lazy as _
from classes.models import YogaClass
from rooms.models import Room
from core.models import Trainer, Trainee
import time
from django.core.exceptions import ValidationError
from lessons.utils import check_overlap_in_list_lesson
from django.db.models import Q
from cards.models import Card
from django.utils.formats import date_format


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
        Room, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('room'),)
    cards = models.ManyToManyField(
        to='cards.Card', through='roll_calls.RollCall', related_name='cards', verbose_name='cards')
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, related_name='lessons', verbose_name=_('trainer'), blank=True, null=True)
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=ACTIVE_STATE, verbose_name=_('state'))
    day = models.DateField(help_text=_(
        'Day of the event'), verbose_name=_('day'))
    start_time = models.TimeField(help_text=_(
        'Starting time'), verbose_name=_('start time'))
    end_time = models.TimeField(help_text=_(
        'Final time'), verbose_name=_('end time'))
    content = models.TextField(help_text=_(
        'Content'), blank=True, null=True, verbose_name=_('content'))
    notes = models.TextField(help_text=_(
        'Notes'), blank=True, null=True, verbose_name=_('notes'))
    is_full = models.BooleanField(default=False, verbose_name=_('is full'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('end at'))

    def __str__(self):
        if self.room:
            return self.yogaclass.name + ' - ' + date_format(self.day, format='SHORT_DATE_FORMAT', use_l10n=True) + ' - ' + self.room.name + ' (' + self.start_time.strftime('%H:%M') + ' - ' + self.end_time.strftime('%H:%M') + ')'
        return self.yogaclass.name + ' - ' + self.start_time.strftime('%H:%M')

    def clean(self):
        room = self.room
        if self.trainer:
            if self.id:
                trainer_lessons_on_day = self.trainer.lessons.filter(
                    day=self.day).exclude(pk=self.id)
            else:
                trainer_lessons_on_day = self.trainer.lessons.filter(
                    day=self.day)
        else:
            if self.id:
                trainer_lessons_on_day = self.yogaclass.form_trainer.lessons.filter(
                    day=self.day).exclude(pk=self.id)
            else:
                trainer_lessons_on_day = self.yogaclass.form_trainer.lessons.filter(
                    day=self.day)
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
        check3 = check_overlap_in_list_lesson(
            self.start_time, self.end_time, trainer_lessons_on_day)
        if any(v['value'] is False for v in [check1, check2, check3]):
            if check1['value'] is False:
                obj = check1['object']
                raise ValidationError(
                    _('overlap time').capitalize() + ': ' + obj.__str__())
            elif check2['value'] is False:
                obj = check2['object']
                raise ValidationError(
                    _('overlap time').capitalize() + ': ' + obj.__str__())
            else:
                obj = check3['object']
                raise ValidationError(
                    _('overlap time for trainer').capitalize() + ': ' + self.trainer.__str__() + ': ' + obj.__str__())

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.id:
            if not self.trainer:
                self.trainer = self.yogaclass.form_trainer
        super(Lesson, self).save(*args, **kwargs)

    def get_time_and_room_detail(self):
        result = '(' + self.start_time.strftime('%H:%M') + \
            ' - ' + self.end_time.strftime('%H:%M') + ')'
        if self.room:
            result += ' - ' + self.room.name
        return result

    def get_time(self):
        result = self.start_time.strftime(
            '%H:%M') + ' - ' + self.end_time.strftime('%H:%M')
        return result

    def get_studied_trainee(self):
        return self.roll_calls.filter(studied=True)

    def get_current_studied_trainee(self):
        studied_number = self.roll_calls.filter(studied=True).count()
        all_enroll_trainee_number = self.roll_calls.all().count()
        result = str(studied_number) + '/' + str(all_enroll_trainee_number)
        return result

    def max_people(self):
        if self.yogaclass.max_people is None:
            return self.room.max_people
        else:
            return min(self.yogaclass.max_people, self.room.max_people)

    def check_is_full(self):
        if self.roll_calls.all().count() < self.max_people():
            return False
        return True

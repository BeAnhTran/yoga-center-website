from datetime import date, datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.classes.models import YogaClass
from apps.rooms.models import Room
from apps.accounts.models import Trainer, Trainee
import time
from django.core.exceptions import ValidationError
from apps.lessons.utils import check_overlap_in_list_lesson
from django.db.models import Q
from apps.cards.models import Card
from django.utils.formats import date_format
from apps.accounts.models import Trainer


ACTIVE_STATE = 0
INACTIVE_STATE = 2

STATE_CHOICES = (
    (ACTIVE_STATE, _('Active')),
    (INACTIVE_STATE, _('Inactive')),
)


class Lesson(models.Model):
    yogaclass = models.ForeignKey(
        YogaClass, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('yogaclass'))
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('room'),)
    lectures = models.ManyToManyField(
        to='lectures.Lecture', related_name='lessons', verbose_name='lectures')
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=ACTIVE_STATE, verbose_name=_('state'))
    date = models.DateField(verbose_name=_('date'))
    start_time = models.TimeField(help_text=_(
        'Starting time'), verbose_name=_('start time'))
    end_time = models.TimeField(help_text=_(
        'Final time'), verbose_name=_('end time'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('notes'))
    is_full = models.BooleanField(default=False, verbose_name=_('is full'))
    substitute_trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, related_name='substitute_lessons', verbose_name=_('substitute trainer'), blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def __str__(self):
        if self.room:
            return self.yogaclass.name + ' - ' + date_format(self.date, format='SHORT_DATE_FORMAT', use_l10n=True) + ' - ' + self.room.name + ' (' + self.start_time.strftime('%H:%M') + ' - ' + self.end_time.strftime('%H:%M') + ')'
        return self.yogaclass.name + ' - ' + self.start_time.strftime('%H:%M')

    def str_without_class(self):
        return date_format(self.date, format='SHORT_DATE_FORMAT', use_l10n=True) + ' - ' + self.room.name + ' (' + self.start_time.strftime('%H:%M') + ' - ' + self.end_time.strftime('%H:%M') + ')'

    def clean(self):
        room = self.room
        trainer = self.yogaclass.trainer
        if self.id:
            trainer_lessons_on_day = Lesson.objects.filter(
                date=self.date, yogaclass__trainer=trainer).exclude(pk=self.id)
            class_lessons_on_day = self.yogaclass.lessons.filter(
                date=self.date).exclude(pk=self.id)
            room_lessons_on_day = room.lessons.filter(
                date=self.date).exclude(pk=self.id)
        else:
            class_lessons_on_day = self.yogaclass.lessons.filter(
                date=self.date)
            room_lessons_on_day = room.lessons.filter(date=self.date)
            trainer_lessons_on_day = Lesson.objects.filter(
                date=self.date, yogaclass__trainer=trainer)

        check1 = check_overlap_in_list_lesson(
            self.start_time, self.end_time, class_lessons_on_day)
        check2 = check_overlap_in_list_lesson(
            self.start_time, self.end_time, room_lessons_on_day)
        check3 = check_overlap_in_list_lesson(
            self.start_time, self.end_time, trainer_lessons_on_day)
        if any(v['value'] is True for v in [check1, check2, check3]):
            if check1['value'] is True:
                obj = check1['object']
                raise ValidationError(
                    _('overlap time').capitalize() + ': ' + obj.__str__())
            elif check2['value'] is True:
                obj = check2['object']
                raise ValidationError(
                    _('overlap time').capitalize() + ': ' + obj.__str__())
            else:
                obj = check3['object']
                raise ValidationError(
                    _('overlap time for trainer').capitalize() + ': ' + self.yogaclass.trainer.__str__() + ': ' + obj.__str__())

    def save(self, *args, **kwargs):
        self.full_clean()
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
        return studied_number

    def max_people(self):
        if self.yogaclass.max_people is None:
            return self.room.max_people
        else:
            return min(self.yogaclass.max_people, self.room.max_people)

    def check_is_full(self):
        if self.get_all_register_trainee_studing() < self.max_people():
            return False
        return True

    # enrolled trainee + make up lesson
    def get_all_register_trainee_studing(self):
        roll_calls_without_make_up_lesson_and_not_have_absence_application = self.roll_calls.filter(
            make_up_lesson=None, absence_application=None).count()
        make_up_lessons_at_this_class = self.make_up_lessons.all().count()
        return roll_calls_without_make_up_lesson_and_not_have_absence_application + make_up_lessons_at_this_class

    def is_in_the_past(self):
        now = datetime.now()
        if self.date < now.date():
            return True
        elif self.date == now.date():
            if self.end_time < now.time():
                return True
            return False
        return False


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

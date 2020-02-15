from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Trainee

FOR_FULL_MONTH = 0
FOR_CONSECUTIVE_LESSONS = 1
FOR_NON_CONSECUTIVE_LESSONS = 2
FOR_TRIAL = 3
FOR_TRAINING_COURSE = 4

FORMS_OF_USING = (
    (FOR_FULL_MONTH, _('Full Month')),
    (FOR_CONSECUTIVE_LESSONS, _('Consecutive Lessons')),
    (FOR_NON_CONSECUTIVE_LESSONS, _('Non Consecutive Lessons')),
    (FOR_TRIAL, _('Trial')),
    (FOR_TRAINING_COURSE, _('For Training Course')),
)


class CardType(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))
    form_of_using = models.IntegerField(choices=FORMS_OF_USING,
                                        default=FOR_FULL_MONTH, verbose_name=_('form of using'))
    min_lessons_require = models.IntegerField(
        null=True, blank=True, verbose_name=_('min lessons required'))
    multiplier = models.FloatField(
        null=True, verbose_name=_('multiplier'))
    for_longtime_trainee_only = models.BooleanField(
        default=False, verbose_name=_('for longtime trainee only'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.name.capitalize()

class Card(models.Model):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='cards', verbose_name=_('trainee'))
    card_type = models.ForeignKey(
        CardType, on_delete=models.CASCADE, related_name='cards', verbose_name=_('card type'))
    start_at = models.DateField(verbose_name=_('start at'))
    end_at = models.DateField(verbose_name=_('end at'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

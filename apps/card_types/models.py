from django.db import models
from django.utils.translation import ugettext_lazy as _

FOR_FULL_MONTH = 0
FOR_SOME_LESSONS = 1
FOR_PERIOD_TIME_LESSONS = 2
FOR_TRIAL = 3
FOR_TRAINING_COURSE = 4

FORMS_OF_USING = (
    (FOR_FULL_MONTH, _('Full Month')),
    (FOR_SOME_LESSONS, _('For Some Lessons')),
    (FOR_PERIOD_TIME_LESSONS, _('For Period Time Lessons')),
    (FOR_TRIAL, _('Trial')),
    (FOR_TRAINING_COURSE, _('For Training Course')),
)


class CardType(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))
    form_of_using = models.IntegerField(choices=FORMS_OF_USING,
                                        default=FOR_FULL_MONTH, verbose_name=_('form of using'))
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

    class Meta:
        unique_together = (('form_of_using', 'for_longtime_trainee_only'),)

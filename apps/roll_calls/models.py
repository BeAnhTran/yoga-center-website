from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.cards.models import Card
from apps.lessons.models import Lesson
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, datetime, timedelta
from django.conf import settings
from apps.card_types.models import FOR_TRAINING_COURSE


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

    def has_make_up_lesson(self):
        try:
            self.make_up_lesson
            return True
        except:
            return False

    def has_refund(self):
        if self.refunds.filter(state__in=[0, 1]).count() > 0:
            return True
        return False

    def has_absence_application(self):
        try:
            self.absence_application
            return True
        except:
            return False

    def is_in_the_past(self):
        now = datetime.now()
        if self.lesson.date < now.date():
            return True
        elif self.lesson.date == now.date():
            if self.lesson.end_time < now.time():
                return True
            return False
        return False

    def is_valid_to_register_make_up_lesson(self):
        if self.lesson.date + timedelta(days=int(settings.NUMBER_OF_EXPIRE_DAYS_FOR_LESSON)) <= datetime.now().date():
            return False
        return True

    # Note: Allow study until expire
    def can_use(self):
        expire = self.card.get_expire_time()
        if self.card.card_type.form_of_using == FOR_TRAINING_COURSE:
            if expire is None:
                return True
            else:
                if type(expire).__name__ == 'date':
                    if self.lesson.date < expire:
                        return True
                else:
                    if self.lesson.date < expire.date():
                        return True
                    elif self.lesson.date == expire.date():
                        if self.lesson.end_time < expire.time():
                            return True
                    else:
                        return False
        else:
            if self.card.is_paid() is False:
                return False
            return True



@receiver(post_save, sender=RollCall)
def cards_changed(sender, instance, **kwargs):
    lesson = instance.lesson
    if lesson.check_is_full():
        lesson.is_full = True
        lesson.save()

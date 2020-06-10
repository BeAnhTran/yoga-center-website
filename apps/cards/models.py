from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import Trainee
from apps.classes.models import YogaClass
from apps.card_types.models import CardType, FOR_FULL_MONTH, FOR_SOME_LESSONS, FOR_TRAINING_COURSE
from apps.common.templatetags import sexify
from django.conf import settings
import math


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

    def start_at(self):
        return self.lessons.order_by('date').first().date

    def end_at(self):
        return self.lessons.order_by('date').last().date

    def total_lesson(self):
        return self.lessons.count()

    def number_of_studied_lesson(self):
        return self.roll_calls.filter(studied=True).count()

    def price_of_one_lesson(self):
        total_price = self.invoices.last().amount
        result = total_price / self.total_lesson()
        return result

    def max_number_of_make_up_lessons(self):
        return math.ceil(self.lessons.all().count() * settings.MAX_NUMBER_OF_MAKE_UP_LESSONS_PERCENTAGE)

    def get_number_of_make_up_lessons(self):
        total = 0
        for r in self.roll_calls.all():
            if r.has_make_up_lesson():
                total += 1
        return total

    def get_number_of_absence_applications(self):
        total = 0
        for r in self.roll_calls.all():
            if r.has_absence_application():
                total += 1
        return total

    def can_register_make_up_lesson(self):
        if self.get_number_of_make_up_lessons() < self.max_number_of_make_up_lessons():
            return True
        return False

    def get_payment_status(self):
        if self.card_type.form_of_using == FOR_TRAINING_COURSE:
            total_amount =  self.yogaclass.get_price_for_training_course()
            if self.yogaclass.payment_periods.all().count() == 0:
                for invoice in self.invoices.all():
                    if invoice.is_charged() is False:
                        return _('Unpaid')
                return _('Paied')
            else:
                result = ''
                for invoice in self.invoices.all():
                    if invoice.is_charged() is True:
                        if invoice.amount == total_amount:
                            return _('Paied')
                        else:
                            result += '\n'
                            result += _('Paied') + ': ' + \
                                invoice.payment_period.name + '(' + str(sexify.sexy_number(invoice.payment_period.amount)) + 'đ)'
                if result == '':
                    return _('Unpaid')
                else:
                    return result
        else:
            for invoice in self.invoices.all():
                if invoice.is_charged() is False:
                    return _('Unpaid')
            return _('Paied')

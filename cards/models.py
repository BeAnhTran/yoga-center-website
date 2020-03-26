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

    def start_at(self):
        return self.lessons.order_by('date').first().date

    def end_at(self):
        return self.lessons.order_by('date').last().date

    def total_lesson(self):
        return self.lessons.count()

    def number_of_studied_lesson(self):
        return self.roll_calls.filter(studied=True).count()


STATE_CHOICES = (
    ('pending', 'Pending'),
    ('approve', 'Approve'),
    ('reject', 'Reject'),
)


class ExtendCardRequest(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='extend_card_requests', verbose_name=_('card')
    )
    new_expire_date = models.DateField(verbose_name=_('new expire date'))
    reason = models.TextField(verbose_name=_('reason'))
    state = models.CharField(max_length=20,
                             choices=STATE_CHOICES,
                             default='pending')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

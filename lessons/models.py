from django.db import models
from django.utils.translation import ugettext_lazy as _
from classes.models import YogaClass
from rooms.models import Room

ACTIVE_STATE = 0
INACTIVE_STATE = 1

STATE_CHOICES = (
    (ACTIVE_STATE, _('Active')),
    (INACTIVE_STATE, _('Inactive')),
)


class Lesson(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.PROTECT, related_name='rooms')
    yogaclass = models.ForeignKey(
        YogaClass, on_delete=models.CASCADE, related_name='classes')
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=ACTIVE_STATE)
    day = models.DateField(help_text=_('Day of the event'))
    start_time = models.TimeField(help_text=_('Starting time'))
    end_time = models.TimeField(help_text=_('Final time'))
    notes = models.TextField(help_text=_('Notes'), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

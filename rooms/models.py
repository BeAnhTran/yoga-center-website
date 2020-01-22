from django.db import models
from django.utils.translation import ugettext_lazy as _

ACTIVE_STATE = 0
INACTIVE_STATE = 1

STATE_CHOICES = (
    (ACTIVE_STATE, _('Active')),
    (INACTIVE_STATE, _('Inactive')),
)


class Room(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    max_people = models.IntegerField()
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=ACTIVE_STATE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

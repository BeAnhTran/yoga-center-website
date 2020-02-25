from django.db import models
from django.utils.translation import ugettext_lazy as _

ACTIVE_STATE = 0
INACTIVE_STATE = 1

STATE_CHOICES = (
    (ACTIVE_STATE, _('Active')),
    (INACTIVE_STATE, _('Inactive')),
)


class Room(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('name'))
    location = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('location'))
    description = models.TextField(
        blank=True, null=True, verbose_name=_('description'))
    max_people = models.IntegerField(verbose_name=_('max people'))
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=ACTIVE_STATE, verbose_name=_('state'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name)

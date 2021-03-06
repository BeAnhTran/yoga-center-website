from django.db import models
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    first_name = models.CharField(max_length=255, verbose_name=_('first name'))
    last_name = models.CharField(max_length=255, verbose_name=_('last name'))
    email = models.EmailField(max_length=255, verbose_name=_('email'))
    phone_number = models.CharField(
        max_length=25, blank=True, null=True, verbose_name=_('phone number'))
    content = models.CharField(max_length=255, verbose_name=_('content'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.content

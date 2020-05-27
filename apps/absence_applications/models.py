from django.db import models
from apps.roll_calls.models import RollCall
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _


class AbsenceApplication(models.Model):
    roll_call = models.OneToOneField(
        RollCall, on_delete=models.CASCADE, primary_key=True, related_name='absence_application')
    reason = models.CharField(max_length=255, verbose_name=_('reason'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

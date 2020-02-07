from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from courses.models import Course
from core.models import Trainer

ACTIVE_STATE = 0
INACTIVE_STATE = 1

STATE_CHOICES = (
    (ACTIVE_STATE, _('Active')),
    (INACTIVE_STATE, _('Inactive')),
)

BASIC_LEVEL = 0
INTERMEDIATE_LEVEL = 1
ADVANCED_LEVEL = 2

LEVEL_CHOICES = (
    (BASIC_LEVEL, _('Basic Level')),
    (INTERMEDIATE_LEVEL, _('Intermediate Level')),
    (ADVANCED_LEVEL, _('Advanced Level')),
)


class YogaClass(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='classes', verbose_name=_('course'))
    form_trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, related_name='classes', verbose_name=_('form_trainer'), blank=True, null=True)
    name = models.CharField(max_length=120, verbose_name=_('name'))
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name=_('slug'))
    description = models.TextField(verbose_name=_('description'))
    image = models.ImageField(
        upload_to='class', blank=True, null=True, verbose_name=_('image'))
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=INACTIVE_STATE, verbose_name=_('state'))
    level = models.IntegerField(choices=LEVEL_CHOICES,
                                default=BASIC_LEVEL, verbose_name=_('level'))
    price_per_lesson = models.FloatField(
        blank=True, null=True, verbose_name=_('price_per_lesson'))
    price_per_month = models.FloatField(
        blank=True, null=True, verbose_name=_('price_per_month'))
    price_course = models.FloatField(
        blank=True, null=True, verbose_name=_('price_course'))
    max_people = models.IntegerField(
        blank=True, null=True, verbose_name=_('max_people'))
    start_at = models.DateField(
        blank=True, null=True, verbose_name=_('start_at'))
    end_at = models.DateField(blank=True, null=True, verbose_name=_('end_at'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated_at'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at', 'name',)
        verbose_name = _('Yoga Class')
        verbose_name_plural = _('Yoga Classes')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(YogaClass, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.name)

    def is_active(self):
        if self.state == ACTIVE_STATE:
            return True
        return False

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from courses.models import Course
from core.models import Trainer
from common.templatetags import sexify
from card_types.models import FOR_TRIAL

DRAFT_STATE = 0
INACTIVE_STATE = 1
ACTIVE_STATE = 2

STATE_CHOICES = (
    (DRAFT_STATE, _('Draft')),
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
        Trainer, on_delete=models.SET_NULL, related_name='classes', verbose_name=_('form trainer'), blank=True, null=True)
    card_types = models.ManyToManyField(
        to='card_types.CardType', related_name='classes', verbose_name=_('card types'))
    name = models.CharField(max_length=120, verbose_name=_('name'))
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name=_('slug'))
    description = models.TextField(verbose_name=_('description'))
    image = models.ImageField(
        upload_to='class', blank=True, null=True, verbose_name=_('image'))
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=DRAFT_STATE, verbose_name=_('state'))
    level = models.IntegerField(
        choices=LEVEL_CHOICES, null=True, verbose_name=_('level'))
    price_per_lesson = models.FloatField(
        blank=True, null=True, verbose_name=_('price per lesson'))
    price_per_month = models.FloatField(
        blank=True, null=True, verbose_name=_('price per month'))
    price_course = models.FloatField(
        blank=True, null=True, verbose_name=_('price course'))
    max_people = models.IntegerField(
        blank=True, null=True, verbose_name=_('max people'))
    start_at = models.DateField(
        blank=True, null=True, verbose_name=_('start at'))
    end_at = models.DateField(blank=True, null=True, verbose_name=_('end at'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

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

    def get_trial_price(self):
        list_trial_card_types = self.card_types.filter(form_of_using=FOR_TRIAL)
        if list_trial_card_types:
            trial_card_type = list_trial_card_types[0]
            if trial_card_type.multiplier is not None and trial_card_type.multiplier > 0:
                if self.price_per_lesson is not None:
                    price = self.price_per_lesson * trial_card_type.multiplier
                    return sexify.sexy_number(price)
                else:
                    return _('have not updated yet')
            else:
                return _('Free')

    def get_price_per_month(self):
        if self.price_per_month is not None:
            if self.price_per_month == int(self.price_per_month):
                self.price_per_month = int(self.price_per_month)
            return sexify.sexy_number(self.price_per_month)
        else:
            return _('have not updated yet')

    def get_price_per_lesson(self):
        if self.price_per_lesson is not None:
            if self.price_per_lesson == int(self.price_per_lesson):
                self.price_per_lesson = int(self.price_per_lesson)
            return sexify.sexy_number(self.price_per_lesson)
        else:
            return _('have not updated yet')
    
    def get_price_course(self):
        if self.price_course is not None:
            if self.price_course == int(self.price_course):
                self.price_course = int(self.price_course)
            return sexify.sexy_number(self.price_course)
        else:
            return _('have not updated yet')

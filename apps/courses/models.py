from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from apps.card_types.models import FOR_TRIAL
from apps.common.templatetags import sexify


PRACTICE_COURSE = 0
TRAINING_COURSE = 1

COURSE_CHOICES = (
    (PRACTICE_COURSE, _('Practice Course')),
    (TRAINING_COURSE, _('Training Course')),
)

BASIC_LEVEL = 0
INTERMEDIATE_LEVEL = 1
ADVANCED_LEVEL = 2

LEVEL_CHOICES = (
    (BASIC_LEVEL, _('Basic Level')),
    (INTERMEDIATE_LEVEL, _('Intermediate Level')),
    (ADVANCED_LEVEL, _('Advanced Level')),
)


class Course(models.Model):
    card_types = models.ManyToManyField(
        to='card_types.CardType', related_name='courses', verbose_name=_('card types'))
    name = models.CharField(max_length=120, verbose_name=_('name'))
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name=_('slug'))
    description = models.CharField(
        max_length=255, verbose_name=_('description'))
    content = RichTextUploadingField(verbose_name=_('content'))
    image = models.ImageField(
        upload_to='course', blank=True, null=True, verbose_name=_('image'))
    course_type = models.IntegerField(choices=COURSE_CHOICES,
                                      default=PRACTICE_COURSE, verbose_name=_('course type'))
    level = models.IntegerField(
        choices=LEVEL_CHOICES, null=True, verbose_name=_('level'))
    price_per_lesson = models.FloatField(
        blank=True, null=True, verbose_name=_('price per lesson'))
    price_per_month = models.FloatField(
        blank=True, null=True, verbose_name=_('price per month'))
    price_for_training_class = models.FloatField(
        blank=True, null=True, verbose_name=_('price for training class'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

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

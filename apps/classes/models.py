from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from apps.courses.models import Course
from apps.accounts.models import Trainer
from apps.common.templatetags import sexify
from apps.card_types.models import FOR_TRIAL
from datetime import datetime, timedelta


class YogaClass(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='classes', verbose_name=_('course'))
    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name='classes', verbose_name=_('trainer'))
    name = models.CharField(max_length=120, verbose_name=_('name'))
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name=_('slug'))
    price_per_lesson = models.FloatField(
        blank=True, null=True, verbose_name=_('price per lesson'))
    price_per_month = models.FloatField(
        blank=True, null=True, verbose_name=_('price per month'))
    price_for_training_class = models.FloatField(
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(YogaClass, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.name)

    def get_price_per_month(self):
        if self.price_per_month is None:
            return self.course.price_per_month
        else:
            return self.price_per_month

    def get_price_per_lesson(self):
        if self.price_per_lesson is None:
            return self.course.price_per_lesson
        else:
            return self.price_per_lesson

    def get_price_for_training_course(self):
        if self.price_for_training_class is None:
            return self.course.price_for_training_class
        else:
            return self.price_for_training_class

    def get_trial_price(self):
        return 0

    def get_first_week(self):
        s = self.lessons.first().date
        result = self.lessons.filter(
            date__range=[s, s + timedelta(days=6)]).order_by('date')
        return result


class PaymentPeriod(models.Model):
    yoga_class = models.ForeignKey(
        YogaClass, on_delete=models.CASCADE, related_name='payment_periods', verbose_name=_('class'))
    name = models.CharField(max_length=120, verbose_name=_('name'))
    amount = models.FloatField(verbose_name=_('amount'))
    end_at = models.DateField(blank=True, null=True, verbose_name=_('end at'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

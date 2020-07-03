from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from apps.courses.models import Course, TRAINING_COURSE
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
    # NOTE: CALCULATE WAGES FOR TRAINER
    wages_per_lesson = models.FloatField(
        blank=True, null=True, verbose_name=_('wages per lesson'))
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

    def get_wages_per_lesson(self):
        if self.wages_per_lesson is None:
            return self.course.wages_per_lesson
        else:
            return self.wages_per_lesson

    def is_training_class(self):
        if self.course.course_type == TRAINING_COURSE:
            return True
        return False

    def can_register_training_class(self):
        if self.course.course_type == TRAINING_COURSE:
            now = datetime.now()
            if self.start_at > now.date():
                return True
            elif self.start_at == now.date():
                if self.lessons.first.start_time > now.time():
                    return True
                else:
                    return False
            else:
                return False
        return False

    def is_happened_training_class(self):
        if self.course.course_type == TRAINING_COURSE:
            now = datetime.now()
            if self.end_at < now.date():
                return True
            else:
                return False
        return False


class PaymentPeriod(models.Model):
    yoga_class = models.ForeignKey(
        YogaClass, on_delete=models.CASCADE, related_name='payment_periods', verbose_name=_('class'))
    name = models.CharField(max_length=120, verbose_name=_('name'))
    amount = models.FloatField(verbose_name=_('amount'))
    end_at = models.DateField(verbose_name=_('end at'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from courses.models import Course

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
        Course, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    image = models.ImageField(
        upload_to='class', blank=True, null=True)
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=ACTIVE_STATE)
    level = models.IntegerField(choices=LEVEL_CHOICES,
                                default=BASIC_LEVEL)
    price_per_lesson = models.FloatField(blank=True, null=True)
    price_per_month = models.FloatField(blank=True, null=True)
    price_course = models.FloatField(blank=True, null=True)
    max_people = models.IntegerField(blank=True, null=True)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at', 'name',)
        verbose_name = 'Yoga Class'
        verbose_name_plural = 'Yoga Classes'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(YogaClass, self).save(*args, **kwargs)

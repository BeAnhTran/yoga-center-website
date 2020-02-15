from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify


PRACTICE_COURSE = 0
TRAINING_COURSE = 1

COURSE_CHOICES = (
    (PRACTICE_COURSE, _('Practice Course')),
    (TRAINING_COURSE, _('Training Course')),
)


class Course(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('name'))
    slug = models.SlugField(max_length=150, unique=True, verbose_name=_('slug'))
    description = models.TextField(verbose_name=_('description'))
    image = models.ImageField(
        upload_to='course', blank=True, null=True, verbose_name=_('image'))
    course_type = models.IntegerField(choices=COURSE_CHOICES,
                                      default=PRACTICE_COURSE, verbose_name=_('course type'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_('end at'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at', 'name',)
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

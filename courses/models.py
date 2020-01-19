from django.db import models
from django.utils.translation import ugettext_lazy as _


PRACTICE_COURSE = 0
TRAINING_COURSE = 1

COURSE_CHOICES = (
    (PRACTICE_COURSE, _('Practice Course')),
    (TRAINING_COURSE, _('Training Course')),
)


class Course(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    gender = models.IntegerField(choices=COURSE_CHOICES,
                                 default=PRACTICE_COURSE)

    def __str__(self):
        return self.name

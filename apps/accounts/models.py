from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.utils.crypto import get_random_string
from apps.certificates.models import Certificate
from apps.card_types.models import FOR_TRAINING_COURSE
from datetime import date, datetime


class User(AbstractUser):
    GENDER_MALE = 0
    GENDER_FEMALE = 1

    GENDER_CHOICES = (
        (GENDER_FEMALE, _('Female')),
        (GENDER_MALE, _('Male')),
    )
    username = None
    email = models.EmailField(
        blank=False, null=False, max_length=254, verbose_name=_('email'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_trainee = models.BooleanField(
        default=False, verbose_name=_('is trainee'))
    is_trainer = models.BooleanField(
        default=False, verbose_name=_('is trainer'))
    first_name = models.CharField(max_length=255, verbose_name=_('first name'))
    last_name = models.CharField(max_length=255, verbose_name=_('last name'))
    slug = models.SlugField(max_length=255, unique=True,
                            verbose_name=_('slug'))
    phone_regex = RegexValidator(
        regex=r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', message="Phone number must be valid")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name=_('phone number'))
    birth_day = models.DateField(
        blank=True, null=True, verbose_name=_('birth day'))
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('address'))
    gender = models.IntegerField(choices=GENDER_CHOICES,
                                 default=GENDER_FEMALE, verbose_name=_('gender'))
    country = CountryField(blank=True, verbose_name=_('country'))
    language = models.CharField(blank=True, null=True,
                                max_length=255, verbose_name=_('language'))
    image = models.ImageField(
        upload_to='profile', blank=True, null=True, verbose_name=_('image'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated_at'))
    certificates = GenericRelation(
        Certificate, related_query_name='users', verbose_name=_('certificates'))

    __original_slug = None

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__original_slug = self.slug

    def full_name(self):
        return self.last_name + ' ' + self.first_name

    def save(self, *args, **kwargs):
        full_name = self.last_name + ' ' + self.first_name
        if not self.slug:
            self.slug = slugify(full_name)
            slug_exists = User.objects.filter(slug__startswith=self.slug)
            if slug_exists.count() > 0:
                temp = self.last_name + self.first_name
                self.slug = self.slug + '-' + str(slug_exists.count() + 1) + get_random_string(
                    length=8, allowed_chars=temp) + str(slug_exists.last().pk)
        else:
            slug = slugify(full_name)
            if self.__original_slug != slug:
                self.slug = slug
                slug_exists = User.objects.filter(slug__startswith=slug)
                if slug_exists.count() > 0:
                    temp = self.first_name + self.last_name
                    self.slug = slug + '-' + str(slug_exists.count() + 1) + get_random_string(
                        length=8, allowed_chars=temp) + str(self.pk)

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name()


PENDING_STATE = 0
APPROVED_STATE = 1
REJECTED_STATE = 2

STATE_CHOICES = (
    (PENDING_STATE, _('pending')),
    (APPROVED_STATE, _('approved')),
    (REJECTED_STATE, _('rejected')),
)


class TemporaryLeaveRequest(models.Model):
    reason = RichTextUploadingField(verbose_name=_('reason'))
    state = models.IntegerField(choices=STATE_CHOICES,
                                default=PENDING_STATE, verbose_name=_('state'))
    leave_at = models.DateField(verbose_name=_('leave at'))
    back_at = models.DateField(verbose_name=_('back at'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name=_('updated at'))

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Trainee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='trainee')
    health_condition = models.TextField(
        blank=True, verbose_name=_('health condition'))
    is_longtime_trainee = models.BooleanField(
        default=False, verbose_name=_('is longtime trainee'))

    def __str__(self):
        result = str(self.pk) + ' - ' + self.full_name() + \
            ' (' + self.user.email + ')'
        return result

    def full_name(self):
        return self.user.last_name + ' ' + self.user.first_name

    def finish_training_class(self):
        check = False
        now = datetime.now()
        for card in self.cards.filter(card_type__form_of_using=FOR_TRAINING_COURSE):
            yoga_class = card.yogaclass
            if yoga_class.end_at > now.date():
                break
            else:
                price_of_training_class = yoga_class.get_price_for_training_course()
                if yoga_class.payment_periods.all().count() == 0:
                    if card.invoices.last().is_charged() is False:
                        break
                    else:
                        return True
                else:
                    total = 0
                    for invoice in card.invoices.all():
                        if invoice.is_charged() is True:
                            total += invoice.amount
                    if total < price_of_training_class:
                        break
                    else:
                        return True
        return check


class Trainer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='trainer')
    introduction = models.TextField(
        null=True, blank=True, verbose_name=_('introduction'))
    experience = RichTextField(
        blank=True, null=True, verbose_name=_('experience'))
    achievements = RichTextUploadingField(
        null=True, blank=True, verbose_name=_('achievements'))
    temporary_leave_requests = GenericRelation(
        TemporaryLeaveRequest, related_query_name='trainers', verbose_name=_('temporary leave requests'))
    is_student = models.BooleanField(
        default=False, verbose_name=_('is student'))
    graduate_school = models.CharField(
        blank=True, null=True, max_length=255, verbose_name=_('graduate school'))
    company_name = models.CharField(
        blank=True, null=True, max_length=255, verbose_name=_('company name'))
    taught_lessons = models.ManyToManyField(
        to='lessons.Lesson', through='lessons.TrainerLesson', related_name='taught_trainer', verbose_name=_('taught lessons'))

    def __str__(self):
        full_name = self.user.full_name()
        return full_name

    def slug(self):
        return self.user.slug


class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='staff')
    experience = RichTextField(blank=True, verbose_name=_('experience'))
    is_student = models.BooleanField(
        default=False, verbose_name=_('is student'))
    graduate_school = models.CharField(
        blank=True, null=True, max_length=255, verbose_name=_('graduate school'))
    company_name = models.CharField(
        blank=True, null=True, max_length=255, verbose_name=_('company name'))
    temporary_leave_requests = GenericRelation(
        TemporaryLeaveRequest, related_query_name='staffs', verbose_name=_('temporary leave requests'))

    def __str__(self):
        full_name = self.user.full_name()
        return full_name

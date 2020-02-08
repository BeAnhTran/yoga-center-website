from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from languages.fields import LanguageField
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_NOT_SPECIFIED = 2

    GENDER_CHOICES = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
        (GENDER_NOT_SPECIFIED, _('Not specified')),
    )
    email = models.EmailField(
        blank=False, null=False, max_length=254, verbose_name='email address', unique=True)
    is_trainee = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(
        regex=r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', message="Phone number must be valid")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True)
    birth_day = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES,
                                 default=GENDER_NOT_SPECIFIED)
    country = CountryField(blank=True)
    language = LanguageField(blank=True, null=True, max_length=55)
    image = models.ImageField(
        upload_to='profile', default='profile/default.png')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def full_name(self):
        return self.first_name + ' ' + self.last_name

class Certificate(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True, max_length=255)
    image = models.ImageField(upload_to='certificate', blank=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Trainee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='trainee')
    health_condition = models.TextField(blank=True)


class Trainer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='trainer')
    yoga_teaching_experience = models.TextField(blank=True)
    yoga_certificates = GenericRelation(Certificate)
    is_student = models.BooleanField(default=False)
    graduate_school = models.CharField(blank=True, null=True, max_length=255)
    company_name = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        full_name = self.user.full_name() 
        return full_name 

class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='staff')
    work_experience = models.TextField(blank=True)
    certificates = GenericRelation(Certificate)
    is_student = models.BooleanField(default=False)
    graduate_school = models.CharField(blank=True, null=True, max_length=255)
    company_name = models.CharField(blank=True, null=True, max_length=255)

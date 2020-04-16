try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction
from faker import Faker
from getenv import env
from datetime import datetime, date, timedelta
from django.utils import timezone
import pytz
import random

from apps.rooms.models import Room
from apps.classes.models import (YogaClass)
from apps.courses.models import (Course, TRAINING_COURSE,
                            PRACTICE_COURSE, BASIC_LEVEL, INTERMEDIATE_LEVEL)
from apps.lessons.models import Lesson
from apps.accounts.models import User, Trainer, Trainee, Staff
from apps.card_types.models import (CardType, FOR_FULL_MONTH,
                               FOR_SOME_LESSONS, FOR_TRIAL, FOR_TRAINING_COURSE)
from apps.cards.models import Card
from apps.roll_calls.models import RollCall
from services.card_invoice_service import CardInvoiceService
from services.roll_call_service import RollCallService
from apps.classes.models import YogaClass


class Command(BaseCommand):
    help = "LOAD SAMPLE DATA INTO THE DB"
    @transaction.atomic
    def handle(self, **options):

        for i, yoga_class in enumerate(YogaClass.objects.filter(course__course_type=PRACTICE_COURSE)):
            _from = i * 5
            _to = _from + 5
            for trainee in Trainee.objects.all()[_from:_to]:
                card = Card.objects.create(**{
                    'trainee': trainee,
                    'yogaclass': yoga_class,
                    'card_type': yoga_class.course.card_types.get(form_of_using=FOR_SOME_LESSONS)
                })
                for lesson in yoga_class.lessons.all()[:12]:
                    RollCall.objects.create(card=card, lesson=lesson)
                price_per_lesson = yoga_class.price_per_lesson
                total = price_per_lesson * card.lessons.all().count()
                CardInvoiceService(card, 'register lessons card', total).call()

        for yoga_class in YogaClass.objects.filter(course__course_type=TRAINING_COURSE)[:1]:
            for trainee in Trainee.objects.order_by('-pk')[:5]:
                card = Card.objects.create(**{
                    'trainee': trainee,
                    'yogaclass': yoga_class,
                    'card_type': yoga_class.course.card_types.get(form_of_using=FOR_TRAINING_COURSE)
                })
                for lesson in yoga_class.lessons.all():
                    RollCall.objects.create(card=card, lesson=lesson)
                price_for_training_class = yoga_class.price_for_training_class
                total = price_for_training_class
                CardInvoiceService(card, 'register lessons card', total).call()

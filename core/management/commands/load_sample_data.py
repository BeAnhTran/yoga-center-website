try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction
from faker import Faker

class Command(BaseCommand):
    help = "Load some sample data into the db"

    @transaction.atomic
    def handle(self, **options):
        from datetime import datetime, date, timedelta
        from django.utils import timezone
        import pytz

        from rooms.models import Room
        from classes.models import YogaClass
        from courses.models import Course
        from lessons.models import Lesson
        from core.models import User, Trainer

        fake = Faker()

        print("Create trainers")
        num_users = User.objects.count()
        if num_users == 0:
            num_users = 1
        for i in range(num_users, num_users + 3):
            data = {
                'username': 'trainer' + str(i),
                'email': 'trainer' + str(i) + '@trainer.com',
                'first_name': fake.first_name(),
                'last_name': fake.last_name()
            }
            trainer = User(**data)
            trainer.set_password('truong77')
            trainer.is_active = True
            trainer.is_staff = False
            trainer.is_trainer = True
            trainer.is_superuser = False
            trainer.save()
            Trainer.objects.create(user=trainer)

        today = timezone.now()
        print("Create some course")
        num_courses = Course.objects.count()
        if num_courses == 0:
            num_courses = 1
        for i in range(num_courses, num_courses + 3):
            data = {
                'name': 'Course ' + str(i),
                'description': 'description ' + str(i)
            }
            course = Course(**data)
            course.save()

        print("Create some classes")
        trainer1 = Trainer.objects.first()
        course1 = Course.objects.first()
        course1.classes.create(
            name='Yoga 1',
            slug='yoga-1',
            description='description class 1',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            form_trainer=trainer1
        )

        print("Create some rooms")
        num_rooms = Room.objects.count()
        if num_rooms == 0:
            num_rooms = 1
        for i in range(num_rooms, num_rooms + 3):
            data = {
                "name": "Room " + str(i),
                "location": "Floor " + str(i),
                "description": "Description room " + str(i),
                "max_people": 10 + i,
                "state": 0,
                "created_at": today,
                "updated_at": today
            }
            room = Room(**data)
            room.save()

        print("Create some lessons")
        room1 = Room.objects.first()
        data = {
            "room_id": room1.id,
            "yogaclass_id": YogaClass.objects.first().id,
            "day": today,
            "start_time": today,
            "end_time": today + timezone.timedelta(hours=1.25)
        }
        lesson1 = Lesson(**data)
        lesson1.save()

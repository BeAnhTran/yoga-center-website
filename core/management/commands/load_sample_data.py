try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load some sample data into the db"

    def handle(self, **options):
        from datetime import datetime, date, timedelta
        from django.utils import timezone
        import pytz

        from rooms.models import Room
        from classes.models import YogaClass
        from courses.models import Course
        from lessons.models import Lesson
        today = timezone.now()

        print("Create some course")
        data = {
            'name': 'Course 1',
            'slug': 'course-1',
            'description': 'description 1'
        }
        course1 = Course(**data)
        course1.save()
        data = {
            'name': 'Course 2',
            'slug': 'course-2',
            'description': 'description 2'
        }
        course2 = Course(**data)
        course2.save()

        print("Create some classes")
        course1.classes.create(
            name='Yoga 1',
            slug='yoga-1',
            description='description class 1',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today
        )

        print("Create some rooms")
        data = {
            "name": "Room 1",
            "location": "Floor 1",
            "description": "",
            "max_people": 10,
            "state": 0,
            "created_at": today,
            "updated_at": today
        }
        room1 = Room(**data)
        room1.save()

        data = {
            "name": "Room 2",
            "location": "Floor 2",
            "description": "",
            "max_people": 12,
            "state": 0,
            "created_at": today,
            "updated_at": today
        }
        room2 = Room(**data)
        room2.save()

        data = {
            "name": "Room 3",
            "location": "Floor 1",
            "description": "",
            "max_people": 15,
            "state": 0,
            "created_at": today,
            "updated_at": today
        }
        room3 = Room(**data)
        room3.save()

        print("Create some lessons")
        data = {
            "room_id": room1.id,
            "yogaclass_id": YogaClass.objects.first().id,
            "day": today,
            "start_time": today,
            "end_time": today + timezone.timedelta(hours=1.25)
        }
        lesson1 = Lesson(**data)
        lesson1.save()

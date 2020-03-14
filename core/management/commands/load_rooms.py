try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction
from getenv import env


class Command(BaseCommand):
    help = "Load some ROOM data into the db"

    @transaction.atomic
    def handle(self, **options):
        from rooms.models import Room
        from faker import Faker
        print("==================")
        print("CREATE ROOMS")
        for i in range(0, int(env('NUMBER_OF_ROOMS'))):
            idx = str(i+1)
            data = {
                "name": "Phòng " + idx,
                "location": "Lầu " + idx,
                "description": "Mô tả cho phòng " + idx,
                "max_people": 20 + i,
                "state": 0,
            }
            room = Room(**data)
            room.save()

        # r = Room.objects.first()
        # r.max_people = 3
        # r.save()

try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load some sample data into the db"

    def handle(self, **options):
        import datetime
        from rooms.models import Room

        today = datetime.date.today()

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

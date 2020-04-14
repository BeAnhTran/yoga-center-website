try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "Load some sample data into the db"

    @transaction.atomic
    def handle(self, **options):
        from apps.core.models import User, Staff
        from faker import Faker
        fake = Faker()
        print("Create staffs")
        num = Staff.objects.count()
        for i in range(num, num + 3):
            data = {
                'email': 'staff' + str(i) + '@gmail.com',
                'first_name': fake.first_name(),
                'last_name': fake.last_name()
            }
            staff = User(**data)
            staff.set_password('truong77')
            staff.is_staff = True
            staff.save()
            Staff.objects.create(user=staff)

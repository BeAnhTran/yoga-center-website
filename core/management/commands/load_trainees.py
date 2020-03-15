try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "Load some sample data into the db"

    @transaction.atomic
    def handle(self, **options):
        from core.models import User, Trainer, Trainee
        from faker import Faker
        fake = Faker()
        print("Create Trainees")
        num = User.objects.count()
        for i in range(num, num + 3):
            data = {
                'email': 'trainee' + str(i) + '@gmail.com',
                'first_name': fake.first_name(),
                'last_name': fake.last_name()
            }
            trainee = User(**data)
            trainee.set_password('truong77')
            trainee.is_trainee = True
            trainee.save()
            Trainee.objects.create(user=trainee)

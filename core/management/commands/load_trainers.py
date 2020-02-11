try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "Load some sample data into the db"

    @transaction.atomic
    def handle(self, **options):
        from core.models import User, Trainer
        from faker import Faker
        fake = Faker()
        print("Create trainers")
        num = User.objects.count()
        for i in range(num, num + 3):
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

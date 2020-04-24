try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "Load some sample data into the db"

    @transaction.atomic
    def handle(self, **options):
        from apps.accounts.models import User, Trainee
        from apps.yoga_stories.models import YogaStory
        from faker import Faker
        fake = Faker()
        print("Create Yoga Stories")
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
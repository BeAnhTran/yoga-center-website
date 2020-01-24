try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load some sample data into the db"

    def handle(self, **options):
        from core.models import User

        print("Create superuser")
        data = {
            'username': 'admin',
            'email': 'admin@admin.com',
        }
        superuser = User(**data)
        superuser.set_password('truong77')
        superuser.is_active = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()

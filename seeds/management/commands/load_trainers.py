try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "Load some sample data into the db"

    @transaction.atomic
    def handle(self, **options):
        from apps.accounts.models import User, Trainer
        print("Create trainers")
        data1 = {
            'email': 'phuongnguyen@gmail.com',
            'first_name': 'Phượng',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/chi_phuong.jpg'
        }
        trainer1 = User(**data1)
        trainer1.set_password('truong77')
        trainer1.is_trainer = True
        trainer1.save()
        Trainer.objects.create(user=trainer1)

        data2 = {
            'email': 'mantue@gmail.com',
            'first_name': 'Mẫn',
            'last_name': 'Tuệ',
            'image': '/seeds/images/trainers/chi_man.jpg'
        }
        trainer2 = User(**data2)
        trainer2.set_password('truong77')
        trainer2.is_trainer = True
        trainer2.save()
        Trainer.objects.create(user=trainer2)

        data3 = {
            'email': 'thanhtien@gmail.com',
            'first_name': 'Tiến',
            'last_name': 'Thanh',
            'image': '/seeds/images/trainers/anh_tien.jpg'
        }
        trainer3 = User(**data3)
        trainer3.set_password('truong77')
        trainer3.is_trainer = True
        trainer3.save()
        Trainer.objects.create(user=trainer3)

        data4 = {
            'email': 'duonghaitan@gmail.com',
            'first_name': 'Tân',
            'last_name': 'Dương',
            'image': '/seeds/images/trainers/anh_tan.jpg'
        }
        trainer4 = User(**data4)
        trainer4.set_password('truong77')
        trainer4.is_trainer = True
        trainer4.save()
        Trainer.objects.create(user=trainer4)

        data5 = {
            'email': 'kieulinh@gmail.com',
            'first_name': 'Linh',
            'last_name': 'Kiều',
            'image': '/seeds/images/trainers/em_linh.jpg'
        }
        trainer5 = User(**data5)
        trainer5.set_password('truong77')
        trainer5.is_trainer = True
        trainer5.save()
        Trainer.objects.create(user=trainer5)

        data6 = {
            'email': 'hoanganh@gmail.com',
            'first_name': 'Anh',
            'last_name': 'Hoàng',
            'image': '/seeds/images/trainers/thay_hoang_anh.jpg'
        }
        trainer6 = User(**data6)
        trainer6.set_password('truong77')
        trainer6.is_trainer = True
        trainer6.save()
        Trainer.objects.create(user=trainer6)

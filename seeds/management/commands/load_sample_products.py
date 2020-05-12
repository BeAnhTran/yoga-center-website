try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "Load some sample data into the db"

    @transaction.atomic
    def handle(self, **options):
        from apps.shop.models import ProductCategory, Product
        from faker import Faker
        print("Create Product Categories")
        category = ProductCategory.objects.create(name='Thảm')
        print("Create Products")
        data = {
            'category': category,
            'name': 'Thảm yoga màu xanh rêu',
            'description': 'thảm yoga màu xanh rêu',
            'quantity': 10,
            'price': 200000,
            'image': 'seeds/shop/tham-yoga-xanh-reu-1.jpg'
        }
        Product.objects.create(**data)

        data = {
            'category': category,
            'name': 'Thảm yoga màu xanh lá cây',
            'description': 'thảm yoga màu xanh lá cây',
            'quantity': 10,
            'price': 200000,
            'image': 'seeds/shop/tham-yoga-xanh-la-cay.jpg'
        }
        Product.objects.create(**data)

        data = {
            'category': category,
            'name': 'Thảm yoga màu hồng',
            'description': 'thảm yoga màu hồng',
            'quantity': 10,
            'price': 200000,
            'image': 'seeds/shop/tham-yoga-hong.jpg'
        }
        Product.objects.create(**data)

import os
from django.conf import settings

try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "LOAD SOME SAMPLE INTO THE DATABASE"

    @transaction.atomic
    def handle(self, **options):
        from getenv import env
        from apps.gallery.models import Gallery, GalleryImage
        path = os.path.join(settings.MEDIA_ROOT, 'seeds/gallery/')
        img_list = os.listdir(path)
        print("Create Gallery")
        gallery = Gallery.objects.create(title='Gallery asasax')
        for img in img_list:
            gallery.images.create(image='seeds/gallery/' + img)

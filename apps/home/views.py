from django.shortcuts import redirect, render
from apps.accounts.models import Trainer
from apps.gallery.models import Gallery


def home(request):
    trainers = Trainer.objects.all()
    gallery = Gallery.objects.first()
    context = {
        'active_nav': 'home',
        'trainers': trainers,
        'gallery': gallery
    }
    return render(request, 'home/index.html', context=context)

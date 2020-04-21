from django.shortcuts import redirect, render
from apps.accounts.models import Trainer
from apps.gallery.models import Gallery
from apps.events.models import Event


def home(request):
    trainers = Trainer.objects.all()
    gallery = Gallery.objects.first()
    events = Event.objects.all()[:3]
    context = {
        'active_nav': 'home',
        'trainers': trainers,
        'gallery': gallery,
        'events': events,
    }
    return render(request, 'home/index.html', context=context)

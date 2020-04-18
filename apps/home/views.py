from django.shortcuts import redirect, render
from apps.accounts.models import Trainer


def home(request):
    trainers = Trainer.objects.all()
    context = {
        'active_nav': 'home',
        'trainers': trainers
    }
    return render(request, 'home/index.html', context=context)

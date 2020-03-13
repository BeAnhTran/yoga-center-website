from django.shortcuts import render
from rooms.models import Room

def index(request):
    context = {
        'active_nav': 'schedule'
    }
    context['rooms'] =  Room.objects.all()
    return render(request, 'yoga_schedule/index.html', context=context)
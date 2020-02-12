from django.shortcuts import render
from rooms.models import Room

def index(request):
    context = {}
    context['rooms'] =  Room.objects.all()
    return render(request, 'yoga_schedule/index.html', context=context)
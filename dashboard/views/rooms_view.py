from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.urls import reverse_lazy

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from ..decorators import admin_required

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from rooms.models import Room
from lessons.models import Lesson

from datetime import datetime
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core import serializers


@method_decorator([login_required, admin_required], name='dispatch')
class RoomListView(ListView):
    model = Room
    template_name = 'dashboard/rooms/list.html'
    context_object_name = 'rooms'
    ordering = ['name']
    paginate_by = 5


@method_decorator([login_required, admin_required], name='dispatch')
class RoomDetailView(DetailView):
    model = Room
    template_name = 'dashboard/rooms/detail.html'
    context_object_name = 'room'


@login_required
@admin_required
def get_lessons(request, pk):
    start_date = datetime.fromisoformat(request.GET['startStr'])
    end_date = datetime.fromisoformat(request.GET['endStr'])

    room = Room.objects.get(pk=pk)
    lessons = room.lessons.filter(day__range=[start_date, end_date])
    data = serializers.serialize(
        'json', lessons, use_natural_foreign_keys=True)
    return HttpResponse(data, content_type="application/json")

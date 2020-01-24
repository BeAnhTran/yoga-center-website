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

import datetime
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core import serializers

@method_decorator([login_required, admin_required], name='dispatch')
class RoomListView(ListView):
    model = Room
    template_name = 'dashboard/room/list.html'
    context_object_name = 'rooms'
    ordering = ['name']
    paginate_by = 5


class RoomDetailView(DetailView):
    model = Room
    template_name = 'dashboard/room/detail.html'
    context_object_name = 'room'


def get_lessons(request, pk):
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)
    room = Room.objects.get(pk=pk)
    lessons = room.lessons.filter(day__range=[start_week, end_week])
    data = serializers.serialize('json', lessons)
    return HttpResponse(data, content_type="application/json")

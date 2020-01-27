from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from ..decorators import admin_required

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from lessons.models import Lesson

from datetime import datetime
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core import serializers

from lessons.models import Lesson


def detail_json(request):
    lesson_id = request.POST['lesson_id']
    lesson = Lesson.objects.get(pk=lesson_id)
    data = serializers.serialize(
        'json', [lesson], use_natural_foreign_keys=True)
    return HttpResponse(data, content_type="application/json")

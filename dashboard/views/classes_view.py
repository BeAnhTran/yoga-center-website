from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required

from classes.models import YogaClass
from ..forms import classes_form, lesssons_form
from courses.models import (PRACTICE_COURSE, TRAINING_COURSE)

from datetime import datetime, timedelta
from django.core import serializers
from django.urls import reverse_lazy
from django.db import transaction
from rest_framework import status
import json
from lessons.serializers.lesson_serializer import LessonSerializer
from rest_framework.response import Response
from dateutil import parser
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


@method_decorator([login_required, admin_required], name='dispatch')
class ClassListView(ListView):
    model = YogaClass
    template_name = 'dashboard/classes/list.html'
    context_object_name = 'classes'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ClassListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'classes'
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class ClassNewView(View):
    template_name = 'dashboard/classes/new.html'

    def get(self, request):
        form = classes_form.ClassNewForm()
        context = {
            'form': form,
            'active_nav': 'classes'
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        form = classes_form.ClassNewForm(request.POST, request.FILES)
        context = {'form': form}

        if form.is_valid():
            form.save()
            return redirect('dashboard:classes-list')

        return render(request, self.template_name, context=context)


@method_decorator([login_required, admin_required], name='dispatch')
class ClassDetailView(DetailView):
    model = YogaClass
    template_name = 'dashboard/classes/show.html'
    context_object_name = 'yogaclass'

    def get_context_data(self, **kwargs):
        context = super(ClassDetailView, self).get_context_data(**kwargs)
        context['active_nav'] = 'classes'
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class ClassScheduleView(DetailView):
    model = YogaClass
    template_name = 'dashboard/classes/schedule.html'
    context_object_name = 'yogaclass'

    def get_context_data(self, **kwargs):
        context = super(ClassScheduleView, self).get_context_data(**kwargs)
        lesson_form = lesssons_form.LessonForm()
        if self.object.trainer:
            lesson_form.fields['trainer'].initial = self.object.trainer
        context['lesson_form'] = lesson_form
        context['active_nav'] = 'classes'
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class ClassEditView(UpdateView):
    model = YogaClass
    template_name = 'dashboard/classes/edit.html'
    slug_field = 'slug'
    form_class = classes_form.ClassEditForm

    def get_success_url(self):
            return reverse('dashboard:classes-list', kwargs={})

    def get_context_data(self, **kwargs):
        context = super(ClassEditView, self).get_context_data(**kwargs)
        context['active_nav'] = 'classes'
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class ClassDeleteView(DeleteView):
    model = YogaClass
    success_url = reverse_lazy('dashboard:classes-list')


@login_required
@admin_required
def get_lessons(request, pk):
    start_date = datetime.fromisoformat(request.GET['startStr'])
    end_date = datetime.fromisoformat(request.GET['endStr'])

    yogaclass = YogaClass.objects.get(pk=pk)
    lessons = yogaclass.lessons.filter(date__range=[start_date, end_date])
    data = serializers.serialize(
        'json', lessons, use_natural_foreign_keys=True)
    return HttpResponse(data, content_type="application/json")


@login_required
@admin_required
def create_lessons(request, pk):
    form = lesssons_form.LessonForm(request.POST, request.FILES)
    if form.is_valid():
        lesson = form.save()
        data = serializers.serialize(
            'json', [lesson], use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")
    return HttpResponse(form.errors.as_json(), status=400)


@login_required
@admin_required
@transaction.atomic
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def create_lessons_from_last_time(request, pk):
    response_data = {}
    yoga_class = YogaClass.objects.get(pk=pk)
    if request.POST['type']:
        try:
            type_create = request.POST['type']
            current_date_calendar = parser.parse(
                request.POST['current_date_calendar'])
            current_entries = []
            if type_create == 'last_week':
                current_start_week = current_date_calendar.date(
                ) - timedelta(current_date_calendar.weekday())
                last_start_week = current_start_week - timedelta(7)
                last_end_week = last_start_week + timedelta(6)
                last_entries = yoga_class.lessons.filter(
                    date__range=[last_start_week, last_end_week])
                if not last_entries:
                    return HttpResponse(_('Last week has no lesson'), status=status.HTTP_400_BAD_REQUEST)
                for last_entry in last_entries:
                    current_entry = last_entry
                    current_entry.pk = None
                    current_entry.day = current_entry.day + timedelta(7)
                    current_entry.save()
                    current_entries.append(current_entry)
            else:
                current_start_week = current_date_calendar.date(
                ) - timedelta(current_date_calendar.weekday())
                last_start_week = current_start_week - timedelta(7)
                last_end_week = last_start_week + timedelta(6)
                last_start_4_weeks = current_start_week - timedelta(28)
                # from (last start 4 weeks) to (last sunday)
                last_entries = yoga_class.lessons.filter(
                    date__range=[last_start_4_weeks, last_end_week])
                if not last_entries:
                    return HttpResponse(_('Last 4 weeks have no lesson'), status=status.HTTP_400_BAD_REQUEST)
                for last_entry in last_entries:
                    current_entry = last_entry
                    current_entry.pk = None
                    current_entry.day = current_entry.day + timedelta(28)
                    current_entry.save()
                    current_entries.append(current_entry)
            serialized = LessonSerializer(current_entries, many=True)
            return Response(serialized.data)
        except Exception as e:
            return HttpResponse(e.messages, status=status.HTTP_400_BAD_REQUEST)
    response_data['message'] = _('Please add type of create')
    return HttpResponse(json.dumps(response_data), status=status.HTTP_400_BAD_REQUEST)

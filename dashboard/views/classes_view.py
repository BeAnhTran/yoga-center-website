from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

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

from datetime import datetime
from django.core import serializers
from django.urls import reverse_lazy


@method_decorator([login_required, admin_required], name='dispatch')
class ClassListView(ListView):
    model = YogaClass
    template_name = 'dashboard/classes/list.html'
    context_object_name = 'classes'
    ordering = ['-updated_at']
    paginate_by = 5


class ClassNewView(View):
    template_name = 'dashboard/classes/new.html'

    def get(self, request):
        form = classes_form.ClassNewForm()
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        form = classes_form.ClassNewForm(request.POST, request.FILES)
        context = {'form': form}

        if form.is_valid():
            form.save()
            return redirect('dashboard:classes-list')

        return render(request, self.template_name, context=context)


class ClassDetailView(DetailView):
    model = YogaClass
    template_name = 'dashboard/classes/show.html'
    context_object_name = 'yogaclass'


class ClassScheduleView(DetailView):
    model = YogaClass
    template_name = 'dashboard/classes/schedule.html'
    context_object_name = 'yogaclass'

    def get_context_data(self, **kwargs):
        context = super(ClassScheduleView, self).get_context_data(**kwargs)
        lesson_form = lesssons_form.LessonForm()
        if self.object.form_trainer:
            lesson_form.fields['trainer'].initial = self.object.form_trainer
        context['lesson_form'] = lesson_form
        return context


class ClassEditView(UpdateView):
    model = YogaClass
    template_name = 'dashboard/classes/edit.html'
    slug_field = 'slug'
    form_class = classes_form.ClassEditForm

    def get_success_url(self):
            return reverse('dashboard:classes-list', kwargs={})


@method_decorator([login_required, admin_required], name='dispatch')
class ClassDeleteView(DeleteView):
    model = YogaClass
    success_url = reverse_lazy('dashboard:classes-list')


def get_lessons(request, pk):
    start_date = datetime.fromisoformat(request.GET['startStr'])
    end_date = datetime.fromisoformat(request.GET['endStr'])

    yogaclass = YogaClass.objects.get(pk=pk)
    lessons = yogaclass.lessons.filter(day__range=[start_date, end_date])
    data = serializers.serialize(
        'json', lessons, use_natural_foreign_keys=True)
    return HttpResponse(data, content_type="application/json")


def create_lessons(request, pk):
    form = lesssons_form.LessonForm(request.POST, request.FILES)
    if form.is_valid():
        lesson = form.save()
        data = serializers.serialize(
            'json', [lesson], use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")
    return HttpResponse(form.errors.as_json(), status=400)

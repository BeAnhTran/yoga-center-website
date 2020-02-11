from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from classes.models import YogaClass, LEVEL_CHOICES
from courses.models import Course
from core.models import Trainer


class YogaClassListView(ListView):
    model = YogaClass
    template_name = 'classes/list.html'
    context_object_name = 'classes'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(YogaClassListView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['levels'] = LEVEL_CHOICES
        context['trainers'] = Trainer.objects.all()
        return context


class YogaClassDetailView(DetailView):
    model = YogaClass
    template_name = 'classes/show.html'
    slug_field = 'slug'
    context_object_name = 'class'

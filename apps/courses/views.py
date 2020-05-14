from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Course


class CourseListView(ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'courses'
    ordering = ['created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'classes'
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/show.html'
    slug_field = 'slug'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        classes = self.object.classes.all()
        context['active_nav'] = 'classes'
        context['classes'] = classes
        return context

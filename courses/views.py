from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Course


class CourseListView(ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'courses'
    ordering = ['created_at']
    paginate_by = 5


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/show.html'
    slug_field = 'slug'
    context_object_name = 'course'

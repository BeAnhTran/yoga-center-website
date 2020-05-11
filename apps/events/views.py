from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from apps.events.models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'events'
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    slug_field = 'slug'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context['active_nav'] = 'events'
        return context

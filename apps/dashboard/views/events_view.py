from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from apps.events.models import Event
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from ..decorators import admin_required
from django.contrib.auth.decorators import login_required
from apps.dashboard.forms import events_form


@method_decorator([login_required, admin_required], name='dispatch')
class EventListView(ListView):
    model = Event
    template_name = 'dashboard/events/list.html'
    context_object_name = 'events'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'events'
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class EventNewView(View):
    template_name = 'dashboard/events/new.html'

    def get(self, request):
        form = events_form.EventForm()
        context = {
            'form': form,
            'active_nav': 'events'
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        form = events_form.EventForm(
            request.POST, request.FILES)
        context = {
            'form': form,
            'active_nav': 'events',
        }

        if form.is_valid():
            form.save()
            return redirect('dashboard:events-list')

        return render(request, self.template_name, context=context)


@method_decorator([login_required, admin_required], name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('dashboard:events-list')

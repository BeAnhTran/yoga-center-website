from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from core.models import Trainer
from django.shortcuts import get_object_or_404
from django.http import Http404


class TrainerListView(ListView):
    model = Trainer
    template_name = 'trainers/list.html'
    context_object_name = 'trainers'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TrainerListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'trainers'
        return context


class TrainerDetailView(DetailView):
    model = Trainer
    template_name = 'trainers/show.html'
    context_object_name = 'trainer'

    def get_object(self):
        slug = self.kwargs['slug']
        try:
            obj = Trainer.objects.get(user__slug=slug)
        except Trainer.DoesNotExist:
            raise Http404("No MyModel matches the given query.")
        return obj

    def get_context_data(self, **kwargs):
        context = super(TrainerDetailView, self).get_context_data(**kwargs)
        context['active_nav'] = 'trainers'
        return context

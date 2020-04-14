from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required

from apps.core.models import (Trainee)


@method_decorator([login_required, admin_required], name='dispatch')
class TraineeListView(ListView):
    model = Trainee
    template_name = 'dashboard/trainees/list.html'
    context_object_name = 'trainees'
    ordering = ['user__date_joined']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TraineeListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'trainees'
        context['show_nav_users'] = True
        return context

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import staff_required

from apps.accounts.models import Trainee
from apps.dashboard.forms.trainees_form import TraineeForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.db import transaction


@method_decorator([login_required, staff_required], name='dispatch')
class TraineeListView(ListView):
    model = Trainee
    template_name = 'dashboard/trainees/list.html'
    context_object_name = 'trainees'
    ordering = ['-user__date_joined']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TraineeListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'trainees'
        context['show_nav_users'] = True
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class TraineeNewView(View):
    template_name = 'dashboard/trainees/new.html'

    def get(self, request):
        context = {}
        form = TraineeForm()
        context['form'] = form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = TraineeForm(request.POST, request.FILES)
        context = {}
        context['form'] = form
        if form.is_valid():
            form.save(request)
            messages.success(self.request, _(
                'Create new trainee successfully'))
            return redirect('dashboard:trainees-list')
        context['active_nav'] = 'trainees'
        context['show_nav_users'] = True
        return render(request, self.template_name, context=context)

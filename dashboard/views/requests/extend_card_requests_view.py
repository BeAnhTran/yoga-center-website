from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views import View

from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from dashboard.decorators import admin_required
from django.db import transaction

from cards.models import (
    ExtendCardRequest, PENDING_STATE, APPROVED_STATE, REJECTED_STATE)
from cards.forms import ExtendCardRequestForm
from cards.serializers import ExtendCardRequestSerializer


@method_decorator([login_required, admin_required], name='dispatch')
class ExtendCardRequestListView(ListView):
    model = ExtendCardRequest
    template_name = 'dashboard/requests/extend_card_requests/list.html'
    context_object_name = 'requests'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ExtendCardRequestListView,
                        self).get_context_data(**kwargs)
        context['active_nav'] = 'extend_card_requests'
        context['show_nav_requests'] = True
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class ExtendCardRequestDetailView(DetailView):
    model = ExtendCardRequest
    template_name = 'dashboard/requests/extend_card_requests/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ExtendCardRequestDetailView,
                        self).get_context_data(**kwargs)
        context['active_nav'] = 'extend_card_requests'
        context['show_nav_requests'] = True
        return context


@login_required
@admin_required
@transaction.atomic
def updateStateOfExtendCardRequest(request, pk):
    obj = get_object_or_404(ExtendCardRequest, pk=pk)
    state = PENDING_STATE
    if request.POST['state'] == 'approve':
        state = APPROVED_STATE
    elif request.POST['state'] == 'reject':
        state = REJECTED_STATE
    obj.state = state
    obj.save()
    return redirect('dashboard:extend-card-requests-list')

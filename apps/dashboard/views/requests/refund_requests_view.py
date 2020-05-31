from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views import View

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.dashboard.decorators import admin_required, staff_required

from apps.refunds.models import Refund
from django.db import transaction


@method_decorator([login_required, staff_required], name='dispatch')
class RefundRequestListView(ListView):
    model = Refund
    template_name = 'dashboard/requests/refund_requests/list.html'
    context_object_name = 'requests'
    order_by = 'created_at'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(RefundRequestListView,
                        self).get_context_data(**kwargs)
        context['active_nav'] = 'refund_requests'
        context['show_nav_requests'] = True
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class RefundRequestDetailView(DetailView):
    model = Refund
    template_name = 'dashboard/requests/refund_requests/detail.html'

    def get_context_data(self, **kwargs):
        context = super(RefundRequestDetailView,
                        self).get_context_data(**kwargs)
        context['active_nav'] = 'refund_requests'
        context['show_nav_requests'] = True
        return context


@login_required
@admin_required
@transaction.atomic
def updateStateOfRefundRequest(request, pk):
    from refunds.models import PENDING_STATE, APPROVED_STATE, REJECTED_STATE
    obj = get_object_or_404(Refund, pk=pk)
    state = PENDING_STATE
    if request.POST['state'] == 'approve':
        state = APPROVED_STATE
    elif request.POST['state'] == 'reject':
        state = REJECTED_STATE
    obj.state = state
    obj.save()
    return redirect('dashboard:refund-requests-list')

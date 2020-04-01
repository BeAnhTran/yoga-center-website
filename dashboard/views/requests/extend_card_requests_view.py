from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views import View

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from dashboard.decorators import admin_required


from cards.models import ExtendCardRequest
from cards.forms import ExtendCardRequestForm


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

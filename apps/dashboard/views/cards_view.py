from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required

from apps.cards.models import Card
from apps.card_invoices.models import PREPAID, POSTPAID


@method_decorator([login_required, staff_required], name='dispatch')
class CardListView(ListView):
    model = Card
    template_name = 'dashboard/cards/list.html'
    context_object_name = 'cards'
    ordering = ['created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CardListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'cards'
        context['show_nav'] = True
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class UnPaidCardListView(ListView):
    model = Card
    template_name = 'dashboard/cards/list.html'
    context_object_name = 'cards'
    ordering = ['created_at']
    paginate_by = 10

    def get_queryset(self):
        query = Card.objects.filter(
            invoice__payment_type=POSTPAID, invoice__staff=None)
        return query

    def get_context_data(self, **kwargs):
        context = super(UnPaidCardListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'unpaid-cards'
        context['show_nav'] = True
        return context

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required

from cards.models import CardType


@method_decorator([login_required, admin_required], name='dispatch')
class CardTypeListView(ListView):
    model = CardType
    template_name = 'dashboard/card_types/list.html'
    context_object_name = 'card_types'
    ordering = ['created_at']
    paginate_by = 5

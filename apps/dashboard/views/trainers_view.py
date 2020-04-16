from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required

from apps.accounts.models import (Trainer)


@method_decorator([login_required, admin_required], name='dispatch')
class TrainerListView(ListView):
    model = Trainer
    template_name = 'dashboard/trainers/list.html'
    context_object_name = 'trainers'
    ordering = ['user__date_joined']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TrainerListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'trainers'
        context['show_nav_users'] = True
        return context

from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required

from apps.core.models import (Staff)


@method_decorator([login_required, admin_required], name='dispatch')
class StaffListView(ListView):
    model = Staff
    template_name = 'dashboard/staffs/list.html'
    context_object_name = 'staffs'
    ordering = ['user__date_joined']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(StaffListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'staffs'
        context['show_nav_users'] = True
        return context

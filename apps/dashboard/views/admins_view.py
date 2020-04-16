from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required

from apps.accounts.models import (User)


@method_decorator([login_required, admin_required], name='dispatch')
class AdminListView(ListView):
    model = User
    template_name = 'dashboard/admins/list.html'
    context_object_name = 'admins'
    ordering = ['user__date_joined']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AdminListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'admins'
        context['show_nav_users'] = True
        return context

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=True)
        return queryset

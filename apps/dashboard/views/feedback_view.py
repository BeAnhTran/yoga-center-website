from django.utils.decorators import method_decorator
from ..decorators import admin_required
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from apps.feedback.models import Feedback


@method_decorator([login_required, admin_required], name='dispatch')
class FeedbackListView(ListView):
    model = Feedback
    template_name = 'dashboard/feedback/list.html'
    context_object_name = 'feedbacks'
    ordering = ['created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FeedbackListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'feedback'
        return context

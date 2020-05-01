from django.utils.decorators import method_decorator
from ..decorators import admin_required
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from apps.questions.models import Question


@method_decorator([login_required, admin_required], name='dispatch')
class QuestionListView(ListView):
    model = Question
    template_name = 'dashboard/questions/list.html'
    context_object_name = 'questions'
    ordering = ['created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'questions'
        return context

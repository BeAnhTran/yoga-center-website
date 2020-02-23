from django.views.generic.list import ListView
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required
from roll_calls.models import RollCall
from lessons.models import Lesson
from datetime import datetime
from django.shortcuts import render


@method_decorator([login_required, staff_required], name='dispatch')
class RollCallListView(ListView):
    model = Lesson
    template_name = 'dashboard/roll_calls/index.html'
    context_object_name = 'lessons'
    paginate_by = 5
    ordering = ['-day']

    def get_context_data(self, **kwargs):
        context = super(RollCallListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'roll_calls'
        return context


class RollCallLessonDetailView(View):
    template_name = 'dashboard/roll_calls/lesson.html'

    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        un_studied_roll_calls = lesson.roll_calls.filter(studied=False)
        studied_roll_calls = lesson.roll_calls.filter(studied=True)

        context = {
            'lesson': lesson,
            'un_studied_roll_calls': un_studied_roll_calls,
            'studied_roll_calls': studied_roll_calls,
            'active_nav': 'roll_calls'
        }
        return render(request, self.template_name, context=context)

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.utils.decorators import method_decorator
from ..decorators import admin_required, staff_required
from django.views.generic.list import ListView
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Trainer
from datetime import datetime


@method_decorator([login_required, staff_required], name='dispatch')
class IndexView(View):
    template_name = 'dashboard/salary/index.html'

    def get(self, request):
        now = datetime.now()
        month = now.month
        year = now.year
        if request.GET.get('month') and request.GET.get('year'):
            month = int(request.GET.get('month'))
            year = int(request.GET.get('year'))
        trainers = Trainer.objects.all()
        data = []
        total = 0
        for trainer in trainers:
            total_of_trainer = 0
            yoga_classes = trainer.classes.filter(
                lessons__date__month=month, lessons__date__year=year).distinct()
            for yoga_class in yoga_classes:
                lessons = yoga_class.lessons.filter(
                    date__month=month, date__year=year)
                number_of_taught_lessons = 0
                for lesson in lessons:
                    if lesson.check_having_trainer() is True and lesson.substitute_trainer is None:
                        number_of_taught_lessons += 1
                total_salary_in_month = number_of_taught_lessons * \
                    yoga_class.get_wages_per_lesson()
                total_of_trainer += total_salary_in_month
            d = {
                'trainer': trainer,
                'total_of_trainer': total_of_trainer,
                'number_of_yoga_classes': yoga_classes.count(),
            }
            data.append(d)
            total += total_of_trainer
        context = {
            'active_nav': 'salary',
            'data': data,
            'month': month,
            'year': year,
            'total': total,
        }
        return render(request, self.template_name, context=context)

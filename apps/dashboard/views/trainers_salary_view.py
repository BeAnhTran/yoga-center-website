from django.shortcuts import render, redirect, reverse, get_object_or_404
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
from apps.classes.models import YogaClass
from datetime import datetime


@method_decorator([login_required, staff_required], name='dispatch')
class IndexView(View):
    template_name = 'dashboard/salary/trainers/index.html'

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
            # SUBSTITUTE LESSONS
            substitute_lessons = trainer.substitute_lessons.filter(date__month=month,date__year=year).distinct()
            for sub in substitute_lessons:
                if sub.check_having_trainer() is True:
                    sub_wages_per_lesson = sub.yogaclass.get_wages_per_lesson()
                    total_of_trainer += sub_wages_per_lesson
            d = {
                'trainer': trainer,
                'total_of_trainer': total_of_trainer,
                'number_of_yoga_classes': yoga_classes.count(),
            }
            data.append(d)
            total += total_of_trainer
        context = {
            'active_nav': 'salary',
            'show_statistic': True,
            'data': data,
            'month': month,
            'year': year,
            'total': total,
        }
        return render(request, self.template_name, context=context)


@method_decorator([login_required, staff_required], name='dispatch')
class DetailListYogaClassView(View):
    template_name = 'dashboard/salary/trainers/list.html'

    def get(self, request, slug):
        trainer = get_object_or_404(Trainer, user__slug=slug)
        now = datetime.now()
        month = now.month
        year = now.year
        if request.GET.get('month') and request.GET.get('year'):
            month = int(request.GET.get('month'))
            year = int(request.GET.get('year'))
        data = []
        total = 0
        class_total = 0
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
            total += total_salary_in_month
            class_total += total_salary_in_month
            d = {
                'yoga_class': yoga_class,
                'number_of_taught_lessons': number_of_taught_lessons,
                'total_salary_in_month': total_salary_in_month,
                'total_lessons_on_month': lessons.count()
            }
            data.append(d)
        
        # SUBSTITUTE LESSONS
        substitute_lessons = trainer.substitute_lessons.filter(date__month=month,date__year=year).distinct()
        data_substitute_lessons = []
        substitute_total = 0
        for sub in substitute_lessons:
            if sub.check_having_trainer() is True:
                sub_class = sub.yogaclass
                sub_wages_per_lesson = sub_class.get_wages_per_lesson()
                total += sub_wages_per_lesson
                substitute_total += sub_wages_per_lesson
                d = {
                    'sub_lesson': sub,
                    'sub_class': sub_class,
                    'sub_wages_per_lesson': sub_wages_per_lesson
                }
                data_substitute_lessons.append(d)

        context = {
            'active_nav': 'salary',
            'show_statistic': True,
            'data': data,
            'month': month,
            'year': year,
            'class_total':class_total,
            'total': total,
            'trainer': trainer,
            'substitute_total': substitute_total,
            'data_substitute_lessons': data_substitute_lessons
        }
        return render(request, self.template_name, context=context)


@method_decorator([login_required, staff_required], name='dispatch')
class DetailYogaClassSalaryView(View):
    template_name = 'dashboard/salary/trainers/detail.html'

    def get(self, request, slug, yoga_class_pk):
        trainer = get_object_or_404(Trainer, user__slug=slug)
        yoga_class = trainer.classes.get(pk=yoga_class_pk)
        now = datetime.now()
        month = now.month
        year = now.year
        if request.GET.get('month') and request.GET.get('year'):
            month = int(request.GET.get('month'))
            year = int(request.GET.get('year'))
        lessons = yoga_class.lessons.filter(date__month=month, date__year=year)
        number_of_taught_lessons = 0
        for lesson in lessons:
            if lesson.check_having_trainer() is True and lesson.substitute_trainer is None:
                number_of_taught_lessons += 1
        total_salary_in_month = number_of_taught_lessons * \
            yoga_class.get_wages_per_lesson()
        context = {
            'active_nav': 'salary',
            'show_statistic': True,
            'month': month,
            'year': year,
            'trainer': trainer,
            'yoga_class': yoga_class,
            'number_of_taught_lessons': number_of_taught_lessons,
            'total_salary_in_month': total_salary_in_month,
            'lessons': lessons
        }
        return render(request, self.template_name, context=context)

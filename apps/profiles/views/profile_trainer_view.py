from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from apps.accounts.decorators import trainer_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.cards.models import Card
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.http import Http404
from apps.refunds.forms import RefundForm
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.db.models import CharField
from apps.make_up_lessons.models import MakeUpLesson
from apps.roll_calls.models import RollCall
from django.conf import settings
from django.utils.formats import date_format
from apps.absence_applications.models import AbsenceApplication
from apps.refunds.models import Refund, PENDING_STATE, APPROVED_STATE
from apps.card_types.models import FOR_TRAINING_COURSE
from apps.classes.models import YogaClass
from datetime import datetime
from apps.profiles.forms.trainer_info_form import TrainerInfoForm


@method_decorator([login_required, trainer_required], name='dispatch')
class TrainerYogaClassView(View):
    template_name = 'profile/trainers/classes/list.html'

    def get(self, request):
        now = datetime.now()
        month = now.month
        year = now.year
        data = []
        if request.GET.get('month') and request.GET.get('year'):
            month = int(request.GET.get('month'))
            year = int(request.GET.get('year'))
        trainer = request.user.trainer
        yoga_classes = trainer.classes.filter(
            lessons__date__month=month, lessons__date__year=year).distinct()
        total = 0
        class_total = 0
        for yoga_class in yoga_classes:
            lessons = yoga_class.lessons.filter(
                date__month=month, date__year=year)
            number_of_taught_lessons = 0
            for lesson in lessons:
                if lesson.check_having_trainer() is True and lesson.substitute_trainer is None:
                    number_of_taught_lessons += 1
            total_salary_in_month = number_of_taught_lessons * \
                yoga_class.get_wages_per_lesson()
            class_total += total_salary_in_month
            total += total_salary_in_month
            d = {
                'yoga_class': yoga_class,
                'number_of_taught_lessons': number_of_taught_lessons,
                'total_lessons_on_month': lessons.count(),
                'total_salary_in_month': total_salary_in_month
            }
            data.append(d)
        # print(data)
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
            'yoga_classes': yoga_classes,
            'sidebar_profile': 'trainers-yoga-classes',
            'month': int(month),
            'year': int(year),
            'data': data,
            'class_total':class_total,
            'total': total,
            'substitute_total': substitute_total,
            'data_substitute_lessons': data_substitute_lessons
        }
        return render(request, self.template_name, context=context)


class TrainerYogaClassDetailView(View):
    template_name = 'profile/trainers/classes/detail.html'

    def get(self, request, slug):
        trainer = request.user.trainer
        yoga_class = get_object_or_404(YogaClass, slug=slug)
        now = datetime.now()
        month = now.month
        year = now.year
        if request.GET.get('month') and request.GET.get('year'):
            month = int(request.GET.get('month'))
            year = int(request.GET.get('year'))
        lessons = yoga_class.lessons.filter(
            date__month=month, date__year=year)
        number_of_taught_lessons = 0
        for lesson in lessons:
            if lesson.check_having_trainer() is True and lesson.substitute_trainer is None:
                number_of_taught_lessons += 1
        total_salary_in_month = number_of_taught_lessons * \
            yoga_class.get_wages_per_lesson()
        context = {
            'yoga_class': yoga_class,
            'trainer': trainer,
            'sidebar_profile': 'trainers-yoga-classes',
            'lessons': lessons,
            'month': int(month),
            'year': int(year),
            'number_of_taught_lessons': number_of_taught_lessons,
            'total_salary_in_month': total_salary_in_month
        }
        return render(request, self.template_name, context=context)


@method_decorator([login_required, trainer_required], name='dispatch')
class TrainerInfoView(View):
    template_name = 'profile/trainers/info/index.html'

    def get(self, request):
        trainer = request.user.trainer
        context = {
            'trainer': trainer,
            'sidebar_profile': 'trainer_info'
        }
        return render(request, self.template_name, context=context)

@method_decorator([login_required, trainer_required], name='dispatch')
class TrainerInfoEditView(View):
    template_name = 'profile/trainers/info/edit.html'

    def get(self, request):
        trainer = request.user.trainer
        form = TrainerInfoForm(instance=trainer)
        context = {
            'trainer': trainer,
            'sidebar_profile': 'trainer_info',
            'form': form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = TrainerInfoForm(
            request.POST, request.FILES, instance=request.user.trainer)
        context = {
            'form': form,
            'active_nav': 'trainer_info',
            'trainer': request.user.trainer,
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thành công')
            return redirect('profile:trainers-info')

        return render(request, self.template_name, context=context)
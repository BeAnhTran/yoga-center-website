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


@method_decorator([login_required, trainer_required], name='dispatch')
class TrainerYogaClassView(View):
    template_name = 'profile/trainers/classes/list.html'

    def get(self, request):
        trainer = request.user.trainer
        yoga_classes = trainer.classes.all()
        context = {
            'yoga_classes': yoga_classes,
            'sidebar_profile': 'trainers-yoga-classes'
        }
        return render(request, self.template_name, context=context)


class TrainerYogaClassDetailView(View):
    template_name = 'profile/trainers/classes/detail.html'

    def get(self, request, slug):
        trainer = request.user.trainer
        yoga_class = get_object_or_404(YogaClass, slug=slug)
        context = {
            'yoga_class': yoga_class,
            'trainer': trainer,
            'sidebar_profile': 'trainers-yoga-classes'
        }
        now = datetime.now()
        month = now.month
        year = now.year
        print("month1", month)
        print("year1", year)
        if request.GET.get('month') and request.GET.get('year'):
            month = int(request.GET.get('month'))
            year = int(request.GET.get('year'))
        print("month2", month)
        print("year2", year)
        lessons = yoga_class.lessons.filter(
            date__month=month, date__year=year)
        print("lessons", lessons)
        context['lessons'] = lessons
        context['month'] = int(month)
        context['year'] = int(year)
        return render(request, self.template_name, context=context)

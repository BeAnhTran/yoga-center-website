from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required

from apps.cards.models import Card
from apps.card_invoices.models import CardInvoice, PREPAID, POSTPAID
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext as _
from apps.courses.models import Course
from apps.classes.models import YogaClass
from apps.dashboard.forms.cards_form import CardForm
from apps.card_types.models import CardType, FOR_FULL_MONTH, FOR_SOME_LESSONS, FOR_TRAINING_COURSE, FOR_TRIAL, FOR_PERIOD_TIME_LESSONS
from apps.lessons.models import Lesson
from apps.common.templatetags import sexify
from apps.classes.utils import get_price, get_total_price, get_total_price_display
from apps.promotions.models import PromotionCode, Promotion, PromotionType, CASH_PROMOTION, PERCENT_PROMOTION, GIFT_PROMOTION, FREE_SOME_LESSON_PROMOTION, PLUS_MONTH_PRACTICE_PROMOTION
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from apps.accounts.models import Trainee
from services.roll_call_service import RollCallService
from apps.card_invoices.models import POSTPAID, PREPAID
from services.card_invoice_service import CardInvoiceService
from django.utils.formats import date_format
from apps.classes.models import YogaClass
from datetime import datetime, timedelta, date
import pytz
import random


def last_day_of_month(any_day):
    next_month = any_day.replace(
        day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


@method_decorator([login_required, staff_required], name='dispatch')
class NewCardListView(ListView):
    model = Card
    template_name = 'dashboard/statistics/new_cards.html'
    context_object_name = 'cards'
    ordering = ['created_at']
    paginate_by = 20

    def get_queryset(self):
        now = datetime.now().date()
        month = now.month
        year = now.year
        if self.request.GET.get('month') and self.request.GET.get('year'):
            month = int(self.request.GET.get('month'))
            year = int(self.request.GET.get('year'))
        first_day_of_month = datetime(year, month, 1).date()
        last_day_of_this_month = last_day_of_month(first_day_of_month)
        query_set = Card.objects.filter(
            created_at__gte=first_day_of_month, created_at__lte=last_day_of_this_month)
        return query_set

    def get_context_data(self, **kwargs):
        now = datetime.now()
        month = now.month
        year = now.year
        if self.request.GET.get('month') and self.request.GET.get('year'):
            month = int(self.request.GET.get('month'))
            year = int(self.request.GET.get('year'))
        context = super(NewCardListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'new-cards-statistic'
        context['show_statistics'] = True
        context['month'] = month
        context['year'] = year
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class NewTraineeListView(ListView):
    model = Trainee
    template_name = 'dashboard/statistics/new_trainees.html'
    context_object_name = 'trainees'
    ordering = ['user__date_joined']
    paginate_by = 20

    def get_queryset(self):
        now = datetime.now().date()
        month = now.month
        year = now.year
        if self.request.GET.get('month') and self.request.GET.get('year'):
            month = int(self.request.GET.get('month'))
            year = int(self.request.GET.get('year'))
        first_day_of_month = datetime(year, month, 1).date()
        last_day_of_this_month = last_day_of_month(first_day_of_month)
        query_set = Trainee.objects.filter(
            user__date_joined__gte=first_day_of_month, user__date_joined__lte=last_day_of_this_month)
        return query_set

    def get_context_data(self, **kwargs):
        context = super(NewTraineeListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'new-trainees-statistic'
        context['show_statistics'] = True
        now = datetime.now().date()
        month = now.month
        year = now.year
        if self.request.GET.get('month') and self.request.GET.get('year'):
            month = int(self.request.GET.get('month'))
            year = int(self.request.GET.get('year'))
        context['month'] = month
        context['year'] = year
        return context


def r(): return random.randint(0, 255)


@method_decorator([login_required, staff_required], name='dispatch')
class RevenueView(View):
    template_name = 'dashboard/statistics/revenue/list.html'

    def get(self, request):
        now = datetime.now().date()
        month = now.month
        year = now.year
        if self.request.GET.get('month') and self.request.GET.get('year'):
            month = int(self.request.GET.get('month'))
            year = int(self.request.GET.get('year'))
        context = {}

        first_day_of_month = datetime(
            year, month, 1, 0, 0, 0, 0, tzinfo=pytz.UTC).date()
        last_day_of_this_month = last_day_of_month(first_day_of_month)

        revenues = []
        total_revenue = 0
        course_colors = []

        for yoga_class in YogaClass.objects.all():
            # if yoga_class.end_at is not None and yoga_class.end_at <= first_day_of_month or yoga_class.start_at is not None and yoga_class.start_at >= last_day_of_this_month:
            #     continue
            d = {}
            d['yoga_class'] = yoga_class
            query_set = CardInvoice.objects.filter(
                created_at__gte=first_day_of_month, created_at__lte=last_day_of_this_month, card__yogaclass=yoga_class)
            total = 0
            number_of_cards = 0
            for invoice in query_set:
                if invoice.is_charged() is True:
                    total += invoice.amount
                    number_of_cards += 1
            total_revenue += total
            d['revenue'] = total
            d['number_of_cards'] = number_of_cards
            revenues.append(d)
            course_colors.append('#%02X%02X%02X' % (r(), r(), r()))

        courses_colors = zip(YogaClass.objects.all(), course_colors)

        context['active_nav'] = 'statistics-revenue'
        context['show_statistics'] = True
        context['revenues'] = revenues
        context['total_revenue'] = total_revenue
        context['month'] = month
        context['year'] = year
        context['course_colors'] = course_colors
        context['courses_colors'] = courses_colors
        return render(request, self.template_name, context=context)


@method_decorator([login_required, staff_required], name='dispatch')
class RevenueDetailView(View):
    template_name = 'dashboard/statistics/revenue/detail.html'

    def get(self, request, pk):
        now = datetime.now().date()
        month = now.month
        year = now.year
        if self.request.GET.get('month') and self.request.GET.get('year'):
            month = int(self.request.GET.get('month'))
            year = int(self.request.GET.get('year'))
        context = {}

        first_day_of_month = datetime(
            year, month, 1, 0, 0, 0, 0, tzinfo=pytz.UTC).date()
        last_day_of_this_month = last_day_of_month(first_day_of_month)

        total_revenue = 0

        yoga_class = get_object_or_404(YogaClass, pk=pk)
        invoices = CardInvoice.objects.filter(
            created_at__gte=first_day_of_month, created_at__lte=last_day_of_this_month, card__yogaclass=yoga_class)
        for invoice in invoices:
            if invoice.is_charged() is True:
                total_revenue += invoice.amount

        context['active_nav'] = 'statistics-revenue'
        context['show_statistics'] = True
        context['month'] = month
        context['year'] = year
        context['yoga_class'] = yoga_class
        context['total_revenue'] = total_revenue
        context['invoices'] = invoices
        return render(request, self.template_name, context=context)

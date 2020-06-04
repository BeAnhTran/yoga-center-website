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
from apps.promotions.models import PromotionCode, Promotion, PromotionType, CASH_PROMOTION, PERCENT_PROMOTION, GIFT_PROMOTION, PLUS_LESSON_PRACTICE_PROMOTION, PLUS_WEEK_PRACTICE_PROMOTION, PLUS_MONTH_PRACTICE_PROMOTION
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from apps.accounts.models import Trainee


@method_decorator([login_required, staff_required], name='dispatch')
class CardListView(ListView):
    model = Card
    template_name = 'dashboard/cards/list.html'
    context_object_name = 'cards'
    ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CardListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'cards'
        context['show_nav'] = True
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class UnPaidCardListView(ListView):
    model = Card
    template_name = 'dashboard/cards/list.html'
    context_object_name = 'cards'
    ordering = ['created_at']
    paginate_by = 10

    def get_queryset(self):
        query = Card.objects.filter(
            invoice__payment_type=POSTPAID, invoice__staff=None)
        return query

    def get_context_data(self, **kwargs):
        context = super(UnPaidCardListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'unpaid-cards'
        context['show_nav'] = True
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class ReceiveCardPaymentView(View):
    def post(self, request, pk):
        invoice = get_object_or_404(CardInvoice, pk=pk)
        with transaction.atomic():
            invoice.staff = request.user.staff
            invoice.save()
            messages.success(request, _('Receive card payment successfully'))
            return redirect('dashboard:unpaid-cards-list')


@method_decorator([login_required, staff_required], name='dispatch')
class CardNewIndexView(ListView):
    template_name = 'dashboard/cards/new/index.html'
    model = YogaClass
    context_object_name = 'classes'
    ordering = ['created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CardNewIndexView, self).get_context_data(**kwargs)
        context['active_nav'] = 'cards'
        context['show_nav'] = True
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class CardNewView(View):
    template_name = 'dashboard/cards/new/create.html'

    def get(self, request, slug):
        yoga_class = get_object_or_404(YogaClass, slug=slug)
        context = {
            'yoga_class': yoga_class,
            'active_nav': 'cards',
            'show_nav': True,
            'form_of_using': -1,
            'FOR_FULL_MONTH': FOR_FULL_MONTH,
            'FOR_PERIOD_TIME_LESSONS': FOR_PERIOD_TIME_LESSONS,
            'FOR_SOME_LESSONS': FOR_SOME_LESSONS,
            'FOR_TRIAL': FOR_TRIAL,
            'FOR_TRAINING_COURSE': FOR_TRAINING_COURSE
        }
        # remove dashboard card form when access enroll page
        if request.session.get('dashboard_card_form') is not None:
            del request.session['dashboard_card_form']
        card_type_list = yoga_class.course.card_types.all()
        form = CardForm(initial={'card_type_list': card_type_list})
        if request.GET.get('card-type'):
            check_card_type_arr = yoga_class.course.card_types.filter(
                pk=request.GET.get('card-type'))
            if check_card_type_arr.count() > 0:
                ctype = check_card_type_arr.first()
                form.fields['card_type'].initial = ctype
                context['form_of_using'] = ctype.form_of_using
            else:
                return redirect('dashboard:cards-new-for-class', slug=slug)
        context['form'] = form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        yoga_class = YogaClass.objects.get(slug=slug)
        card_type_list = yoga_class.course.card_types.all()
        context = {
            'yoga_class': yoga_class,
            'active_nav': 'cards',
            'show_nav': True,
            'form_of_using': -1,
            'FOR_FULL_MONTH': FOR_FULL_MONTH,
            'FOR_PERIOD_TIME_LESSONS': FOR_PERIOD_TIME_LESSONS,
            'FOR_SOME_LESSONS': FOR_SOME_LESSONS,
            'FOR_TRIAL': FOR_TRIAL,
            'FOR_TRAINING_COURSE': FOR_TRAINING_COURSE
        }
        form = CardForm(
            request.POST, initial={'card_type_list': card_type_list})
        print(form.is_valid())
        if form.is_valid():
            if self.check_valid_lessons(form) is False:
                messages.error(request, _(
                    'Trainee have had one of this lessons before'))
                return redirect('dashboard:cards-new-for-class', slug=slug)
            # save to session and get it in payment page
            request.session['dashboard_card_form'] = request.POST
            return redirect('dashboard:cards-new-for-class-preview', slug=slug)
        ctype = yoga_class.course.card_types.filter(
            pk=request.POST['card_type']).first()
        form.fields['card_type'].initial = ctype
        context['form'] = form
        context['form_of_using'] = ctype.form_of_using
        return render(request, self.template_name, context=context)

    def check_valid_lessons(self, form):
        trainee_pk = form.cleaned_data['trainee']
        lesson_id_arr = eval(form.cleaned_data['lesson_list'])
        c = Card.objects.filter(trainee__pk=trainee_pk,
                                lessons__pk__in=lesson_id_arr).distinct()
        if c:
            return False
        return True


@method_decorator([login_required, staff_required], name='dispatch')
class CardNewPreviewView(View):
    template_name = 'dashboard/cards/new/preview.html'

    def get(self, request, slug):
        if request.session.get('dashboard_card_form'):
            yoga_class = YogaClass.objects.get(slug=slug)
            dashboard_card_form = request.session['dashboard_card_form']
            trainee = get_object_or_404(Trainee, pk=dashboard_card_form['trainee'])
            lesson_list = self.__lesson_list_available(
                yoga_class, dashboard_card_form)
            card_type = CardType.objects.get(
                pk=dashboard_card_form['card_type'])
            price = get_price(yoga_class, card_type)
            total_price = get_total_price(
                yoga_class, card_type, lesson_list.count())
            total_price_display = get_total_price_display(total_price)
            context = {
                'yoga_class': yoga_class,
                'trainee':trainee,
                'card_type': card_type,
                'lesson_list': lesson_list,
                'price': price,
                'total_price_display': total_price_display,
                'total_price': total_price,
                'active_nav': 'cards',
                'show_nav': True,
                'FOR_FULL_MONTH': FOR_FULL_MONTH,
                'FOR_PERIOD_TIME_LESSONS': FOR_PERIOD_TIME_LESSONS,
                'FOR_SOME_LESSONS': FOR_SOME_LESSONS,
                'FOR_TRIAL': FOR_TRIAL,
                'FOR_TRAINING_COURSE': FOR_TRAINING_COURSE
            }
            # PROMOTION
            promotion_type = None
            promotion_code = None
            promotion_val = 'không'
            amount = total_price
            if request.session.get('dashboard_promotion_code') and request.session.get('dashboard_promotion_type'):
                # get promotion type
                promotion_type = get_object_or_404(
                    PromotionType, pk=request.session.get('dashboard_promotion_type'))
                # get promotion code
                promotion_code = get_object_or_404(
                    PromotionCode, pk=request.session.get('dashboard_promotion_code'))
                value = int(promotion_type.value)
                if promotion_type.category == CASH_PROMOTION:
                    amount -= value
                    promotion_val = '-' + \
                        sexify.sexy_number(value) + 'đ'
                elif promotion_type.category == PERCENT_PROMOTION:
                    amount -= value*amount/100
                    promotion_val = '-' + \
                        sexify.sexy_number(value*amount) + 'đ'
                elif promotion_type.category == PLUS_LESSON_PRACTICE_PROMOTION:
                    promotion_lessons = yoga_class.lessons.filter(
                        date__gt=lesson_list.last().date, is_full=False).order_by('date')[:value]
                    context['promotion_lessons'] = promotion_lessons
                elif promotion_type.category == PLUS_WEEK_PRACTICE_PROMOTION:
                    s = lesson_list.last().date
                    promotion_lessons = yoga_class.lessons.filter(
                        date__gt=s, date__lte=s + timedelta(days=7*value), is_full=False).order_by('date')
                    context['promotion_lessons'] = promotion_lessons
                elif promotion_type.category == PLUS_MONTH_PRACTICE_PROMOTION:
                    s = lesson_list.last().date
                    promotion_lessons = yoga_class.lessons.filter(
                        date__gt=s, date__lte=s + relativedelta(months=value), is_full=False).order_by('date')
                    context['promotion_lessons'] = promotion_lessons
                else:
                    promotion_val = promotion_type.full_title
            amount_display = sexify.sexy_number(amount)
            context['dashboard_promotion_type'] = promotion_type
            context['dashboard_promotion_code'] = promotion_code
            context['dashboard_promotion_val'] = promotion_val
            context['amount'] = amount
            context['amount_display'] = amount_display
            return render(request, self.template_name, context=context)
        else:
            messages.error(request, _(
                'Dont have any info about card. Please try again'))
            return redirect('dashboard:cards-new-for-class', slug=slug)

    def __lesson_list_available(self, yoga_class, form):
        cleaned_data = CardForm(form).cleaned_data
        id_arr = eval(cleaned_data['lesson_list'])
        lesson_list = yoga_class.lessons.filter(
            is_full=False, pk__in=id_arr).order_by('date')
        return lesson_list

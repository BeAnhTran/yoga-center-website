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
    model = CardInvoice
    template_name = 'dashboard/cards/unpaid_list.html'
    context_object_name = 'invoices'
    ordering = ['created_at']
    paginate_by = 10

    def get_queryset(self):
        query = CardInvoice.objects.filter(charge_id=None, staff=None)
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
            # return redirect('dashboard:unpaid-cards-list')
            return redirect('dashboard:cards-new-for-class-result', pk=invoice.card.pk)


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
                if request.GET.get('trainee-id'):
                    check_trainee = Trainee.objects.filter(
                        pk=request.GET.get('trainee-id'))
                    if check_trainee.count() == 1:
                        form.fields['trainee'].initial = check_trainee.first()
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
        if form.is_valid():
            # CHECK THAT HAVING OLD LESSON IN LESSON LIST
            id_arr = eval(request.POST['lesson_list'])
            lesson_list = yoga_class.lessons.filter(
                is_full=False, pk__in=id_arr).order_by('date')
            for l in lesson_list:
                if l.is_in_the_past() is True:
                    messages.error(request, _(
                        'Your lesson list includes old lesson. Please try again.'))
                    return redirect(reverse('dashboard:cards-new-for-class', kwargs={'slug': slug}) + '?card-type=' + request.POST['card_type'] + '&trainee-id=' + request.POST['trainee'])
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
            trainee = get_object_or_404(
                Trainee, pk=dashboard_card_form['trainee'])
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
                'trainee': trainee,
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
                elif promotion_type.category == FREE_SOME_LESSON_PROMOTION:
                    promotion_lessons = yoga_class.lessons.filter(
                        date__gt=lesson_list.last().date, is_full=False).order_by('date')[:value]
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

    @transaction.atomic
    def post(self, request, slug):
        yoga_class = YogaClass.objects.get(slug=slug)
        if request.session.get('dashboard_card_form'):
            form = CardForm(request.session['dashboard_card_form'])
            if form.is_valid():
                trainee = get_object_or_404(
                    Trainee, pk=form.cleaned_data['trainee'])
                amount = request.POST.get('amount')
                #
                # PROMOTION
                promotion_type = None
                promotion_code = None
                if request.session.get('dashboard_promotion_code') and request.session.get('dashboard_promotion_type'):
                    promotion_type = get_object_or_404(
                        PromotionType, pk=request.session.get('dashboard_promotion_type'))
                    promotion_code = get_object_or_404(
                        PromotionCode, pk=request.session.get('dashboard_promotion_code'))
                # CREATE CARD
                card = self.create_card(
                    yoga_class, form, trainee, promotion_code, promotion_type)
                # CREATE CARD INVOICE
                description = _('Create new card at center')
                card_invoice = CardInvoiceService(
                    card, POSTPAID, description, amount, None).call()
                card_invoice.staff = request.user.staff
                card_invoice.save()

                if promotion_code is not None and promotion_type is not None:
                    promotion_code.promotion_type = promotion_type
                    promotion_code.save()
                    if promotion_type.category == GIFT_PROMOTION:
                        promotion_code.promotion_code_products.create(
                            product=promotion_type.product, quantity=promotion_type.value)
                    card_invoice.apply_promotion_codes.create(
                        promotion_code=promotion_code)
                if request.session.get('dashboard_card_form'):
                    del request.session['dashboard_card_form']
                if request.session.get('dashboard_promotion_code'):
                    del request.session['dashboard_promotion_code']
                if request.session.get('dashboard_promotion_type'):
                    del request.session['dashboard_promotion_type']
                return redirect('dashboard:cards-new-for-class-result', pk=card.pk)
            else:
                messages.error(request, _(
                    'An error occurred. Please try again later'))
                return redirect('dashboard:cards-new-for-class', slug=slug)
        else:
            messages.error(request, _(
                'Dont have any info about card. Please try again'))
            return redirect('dashboard:cards-new-for-class', slug=slug)

    def __lesson_list_available(self, yoga_class, form):
        f = CardForm(form)
        if f.is_valid():
            id_arr = eval(f.cleaned_data['lesson_list'])
            lesson_list = yoga_class.lessons.filter(
                is_full=False, pk__in=id_arr).order_by('date')
            return lesson_list
        return []

    @transaction.atomic
    def create_card(self, yoga_class, form, trainee, promotion=None, promotion_type=None):
        # TODO: Start_at and end_at: only having in FULL MONTH
        if promotion is not None and promotion_type is not None:
            if promotion_type.category == PLUS_MONTH_PRACTICE_PROMOTION:
                start = form.cleaned_data['start_at']
                end = form.cleaned_data['end_at']
                month_count = int(promotion_type.value)
                end = end + relativedelta(months=month_count)
        # lesson_list = yoga_class.lessons.filter(date__range=[start, end])
        id_arr = eval(form.cleaned_data['lesson_list'])
        lesson_list = yoga_class.lessons.filter(
            is_full=False, pk__in=id_arr).order_by('date')
        card = form.save(commit=False)
        card.trainee = trainee
        card.yogaclass = yoga_class
        card.save()
        RollCallService(card, lesson_list).call()
        return card


@method_decorator([login_required, staff_required], name='dispatch')
class CardNewResultView(View):
    template_name = 'dashboard/cards/new/result.html'

    def get(self, request, pk):
        context = {}
        card = get_object_or_404(
            Card, pk=pk)
        context['yoga_class'] = card.yogaclass
        context['paymentType'] = 'Postpaid'
        context['card'] = card
        charged_str = card.get_payment_status()

        card_str_qrcode = '''Tên: {fname}\nEmail: {femail}\nMã số thẻ: {fcard_id}\nTên lớp: {fclass_name}\nLoại thẻ: {fcard_type}\nNgày bắt đầu: {fstart_at}\nNgày kết thúc: {fend_at}\nTrạng thái: {fis_charged}'''.format(
            fname=card.trainee.user.full_name(),
            femail=card.trainee.user.email,
            fcard_id=card.pk,
            fclass_name=card.yogaclass.name,
            fcard_type=card.card_type.name,
            fstart_at=date_format(
                card.start_at(), format='SHORT_DATE_FORMAT', use_l10n=True),
            fend_at=date_format(
                card.end_at(), format='SHORT_DATE_FORMAT', use_l10n=True),
            fis_charged=charged_str
        )
        context['card_str_qrcode'] = card_str_qrcode
        return render(request, self.template_name, context=context)

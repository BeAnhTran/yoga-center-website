# -*- coding: utf-8 -*-
import uuid
from services.sms_service import send_twilio_message
from services.stripe_service import StripeService
from services.momo_service import MoMoService, MoMoResponseService
import json
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

from apps.courses.models import LEVEL_CHOICES, TRAINING_COURSE
from apps.classes.models import YogaClass
from apps.courses.models import Course
from apps.accounts.models import Trainer

from django.db.models import Q
from apps.cards.forms import CardFormForTraineeEnroll

from rest_framework.views import APIView
from rest_framework.response import Response
from apps.lessons.serializers.lesson_serializer import LessonSerializer
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.accounts.decorators import trainee_required

from django.conf import settings

from rest_framework import status
from django.http import HttpResponse
from apps.payment.form import CardPaymentForm

from apps.card_types.models import (CardType,
                                    FOR_FULL_MONTH, FOR_SOME_LESSONS, FOR_TRAINING_COURSE, FOR_TRIAL,
                                    FOR_PERIOD_TIME_LESSONS)

from apps.common.templatetags import sexify
from apps.classes.utils import get_price, get_total_price, get_total_price_display
from django.db import transaction
from services.card_invoice_service import CardInvoiceService
from services.roll_call_service import RollCallService
from django.contrib import messages
from apps.classes.forms import FilterForm
from django.db.models import Value as V
from django.db.models.functions import Concat
from apps.promotions.models import PromotionCode, Promotion, PromotionType, CASH_PROMOTION, PERCENT_PROMOTION, \
    GIFT_PROMOTION, FREE_SOME_LESSON_PROMOTION, PLUS_MONTH_PRACTICE_PROMOTION
from apps.roll_calls.models import RollCall
from apps.card_invoices.models import POSTPAID, PREPAID
from apps.cards.models import Card
from apps.common.tasks import removeCardWhenNotPayed
from django.utils import timezone


class YogaClassListView(ListView):
    model = YogaClass
    template_name = 'classes/list.html'
    context_object_name = 'classes'
    ordering = ['created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        query_course = list(((None, 'Chọn khóa học'),)) + \
                       list(Course.objects.values_list('slug', 'name'))
        query_trainer = list(((None, 'Chọn huấn luyện viên'),)) + list(Trainer.objects.annotate(
            full_name=Concat('user__last_name', V(' '), 'user__first_name')).values_list('user__slug', 'full_name'))

        context = super(YogaClassListView, self).get_context_data(**kwargs)
        form_filter = FilterForm(
            initial={
                'query_course': query_course,
                'query_trainer': query_trainer
            }
        )
        if self.request.GET.get('course'):
            form_filter.fields['course'].initial = self.request.GET.get(
                'course')
        if self.request.GET.get('trainer'):
            form_filter.fields['trainer'].initial = self.request.GET.get(
                'trainer')
        if self.request.GET.get('level'):
            form_filter.fields['level'].initial = self.request.GET.get('level')
        context['form_filter'] = form_filter
        context['active_nav'] = 'classes'
        return context

    def get_queryset(self):
        filter_options = {}
        if self.request.GET.get('course'):
            filter_options['course__slug'] = self.request.GET.get('course')
        if self.request.GET.get('trainer'):
            filter_options['trainer__user__slug'] = self.request.GET.get(
                'trainer')
        if self.request.GET.get('level'):
            filter_options['course__level'] = self.request.GET.get('level')
        queryset = YogaClass.objects.filter(
            **filter_options).order_by('created_at')
        return queryset


class YogaClassDetailView(DetailView):
    model = YogaClass
    template_name = 'classes/show.html'
    slug_field = 'slug'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super(YogaClassDetailView, self).get_context_data(**kwargs)
        context['active_nav'] = 'classes'
        lesson = self.object.lessons.first()
        tdelta = datetime.combine(
            date.today(), lesson.end_time) - datetime.combine(date.today(), lesson.start_time)
        duration = int(tdelta.total_seconds() / 60)
        context['duration'] = duration
        context['others'] = set(
            YogaClass.objects.filter(~Q(pk=self.object.pk)))
        return context


class YogaClassEnrollView(View):
    template_name = 'classes/enroll.html'

    def get(self, request, slug):
        if request.session.get('promotion_code'):
            del request.session['promotion_code']
        if request.session.get('promotion_type'):
            del request.session['promotion_type']
        yoga_class = YogaClass.objects.get(slug=slug)
        context = {
            'yoga_class': yoga_class,
            'active_nav': 'classes',
            'form_of_using': -1,
            'FOR_FULL_MONTH': FOR_FULL_MONTH,
            'FOR_PERIOD_TIME_LESSONS': FOR_PERIOD_TIME_LESSONS,
            'FOR_SOME_LESSONS': FOR_SOME_LESSONS,
            'FOR_TRIAL': FOR_TRIAL,
            'FOR_TRAINING_COURSE': FOR_TRAINING_COURSE
        }
        price_arr = {}
        for card_type in yoga_class.course.card_types.all():
            price = get_price(yoga_class, card_type)
            if card_type.form_of_using == FOR_FULL_MONTH:
                price_arr['FOR_FULL_MONTH'] = price
            elif card_type.form_of_using == FOR_PERIOD_TIME_LESSONS:
                price_arr['FOR_PERIOD_TIME_LESSONS'] = price
            elif card_type.form_of_using == FOR_SOME_LESSONS:
                price_arr['FOR_SOME_LESSONS'] = price
            elif card_type.form_of_using == FOR_TRIAL:
                price_arr['FOR_TRIAL'] = price
            elif card_type.form_of_using == FOR_TRAINING_COURSE:
                price_arr['FOR_TRAINING_COURSE'] = price
        context['price_arr'] = price_arr
        # remove enroll card form when access enroll page
        if request.session.get('enroll_card_form') is not None:
            del request.session['enroll_card_form']
        card_type_list = yoga_class.course.card_types.all()

        if yoga_class.course.course_type == TRAINING_COURSE:
            print(list(yoga_class.lessons.filter().values_list(
                'id', flat=True).distinct()))
            payment_period_choices = [(0, _('Pay all'))]
            if yoga_class.payment_periods.all().count() > 0:
                first_payment_period = yoga_class.payment_periods.all().order_by('end_at').first()
                payment_period_choices.append(
                    (first_payment_period.id, first_payment_period.name), )
            form = CardFormForTraineeEnroll(initial={
                'card_type_list': card_type_list, 'payment_period_choices': payment_period_choices})
            form.fields['payment_period'].initial = 0
            form.fields['lesson_list'].initial = str(
                list(yoga_class.lessons.filter().values_list('id', flat=True).distinct()))
            form.fields['card_type'].initial = yoga_class.course.card_types.first()
            context['form_of_using'] = yoga_class.course.card_types.first(
            ).form_of_using
        else:
            form = CardFormForTraineeEnroll(
                initial={'card_type_list': card_type_list})

        if request.GET.get('card-type'):
            check_card_type_arr = yoga_class.course.card_types.filter(
                pk=request.GET.get('card-type'))
            if check_card_type_arr.count() > 0:
                ctype = check_card_type_arr.first()
                form.fields['card_type'].initial = ctype
                context['form_of_using'] = ctype.form_of_using
            else:
                return redirect('classes:enroll', slug=slug)
        context['form'] = form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        yoga_class = YogaClass.objects.get(slug=slug)
        card_type_list = yoga_class.course.card_types.all()
        card_type = CardType.objects.get(pk=request.POST.get('card_type'))
        context = {
            'yoga_class': yoga_class,
            'active_nav': 'classes',
            'form_of_using': -1,
            'FOR_FULL_MONTH': FOR_FULL_MONTH,
            'FOR_PERIOD_TIME_LESSONS': FOR_PERIOD_TIME_LESSONS,
            'FOR_SOME_LESSONS': FOR_SOME_LESSONS,
            'FOR_TRIAL': FOR_TRIAL,
            'FOR_TRAINING_COURSE': FOR_TRAINING_COURSE
        }
        if yoga_class.course.course_type == TRAINING_COURSE:
            payment_period_choices = [(0, _('Pay all'))]
            if yoga_class.payment_periods.all().count() > 0:
                first_payment_period = yoga_class.payment_periods.all().order_by('end_at').first()
                payment_period_choices.append(
                    (first_payment_period.id, first_payment_period.name), )
            form = CardFormForTraineeEnroll(
                request.POST,
                initial={'card_type_list': card_type_list, 'payment_period_choices': payment_period_choices})
        else:
            form = CardFormForTraineeEnroll(
                request.POST, initial={'card_type_list': card_type_list})
        if form.is_valid():
            id_arr = eval(request.POST['lesson_list'])
            lesson_list = yoga_class.lessons.filter(
                is_full=False, pk__in=id_arr).order_by('date')
            # CHECK THAT HAVING OLD LESSON IN LESSON LIST
            for l in lesson_list:
                if l.is_in_the_past() is True:
                    messages.error(request, _(
                        'Your lesson list includes old lesson. Please try again.'))
                    return redirect(
                        reverse('classes:enroll', kwargs={'slug': slug}) + '?card-type=' + request.POST['card_type'])
            # NOTE: check lessons of FOR_SOME_LESSONS
            if card_type.form_of_using == FOR_SOME_LESSONS:
                i = 0
                while i < (len(lesson_list) - 1):
                    current_lesson = lesson_list[i]
                    next_index = i + 1
                    next_lesson = lesson_list[next_index]
                    check_list = yoga_class.lessons.filter(
                        date__gt=current_lesson.date, date__lt=next_lesson.date, is_full=False)
                    if len(check_list) > 2:
                        messages.error(
                            request,
                            'Hai buổi tập đăng ký liên tiếp trong thẻ không được cách nhau quá 2 buổi trống khác.')
                        return redirect('classes:enroll', slug=slug)
                    i += 1

            # save to session and get it in payment page
            request.session['enroll_card_form'] = request.POST
            return redirect('classes:enroll-payment', slug=slug)
        # IF form is NOT VALID
        if yoga_class.course.course_type == TRAINING_COURSE:
            form.fields['card_type'].initial = yoga_class.course.card_types.first()
            form.fields['lesson_list'].initial = str(
                list(yoga_class.lessons.filter().values_list('id', flat=True)))
            context['form_of_using'] = yoga_class.course.card_types.first(
            ).form_of_using
            form.fields['payment_period'].initial = 0
        else:
            ctype = yoga_class.course.card_types.filter(
                pk=request.POST['card_type']).first()
            form.fields['card_type'].initial = ctype
            context['form_of_using'] = ctype.form_of_using
        context['form'] = form
        return render(request, self.template_name, context=context)


class YogaClassGetLessonListView(APIView):
    # Get List Lesson for specified Yoga Class in range time
    def get(self, request, slug):
        obj = YogaClass.objects.get(slug=slug)
        start_date = datetime.fromisoformat(request.GET['startStr'])
        end_date = datetime.fromisoformat(request.GET['endStr'])
        lessons = obj.lessons.filter(date__range=[start_date, end_date])
        serialized = LessonSerializer(lessons, many=True)
        return Response(serialized.data)


@method_decorator([login_required, trainee_required], name='dispatch')
class YogaClassEnrollPaymentView(View):
    template_name = 'payment.html'

    def get(self, request, slug):
        if request.session.get('enroll_card_form'):
            yoga_class = YogaClass.objects.get(slug=slug)
            enroll_card_form = request.session['enroll_card_form']
            card_type = CardType.objects.get(pk=enroll_card_form['card_type'])
            lesson_list = self.__lesson_list_available(
                yoga_class, enroll_card_form)
            # NOTE: check da dang ky buoi tap
            for l in lesson_list:
                if l.roll_calls.filter(card__trainee=request.user.trainee).count() > 0:
                    messages.error(
                        request, _('You have card including one of your choosen lesson list. Please check your card.'))
                    return redirect('classes:enroll', slug=slug)
            # Payment Form
            form = CardPaymentForm()
            context = {
                'key': settings.STRIPE_PUBLISHABLE_KEY,
                'form': form,
                'yoga_class': yoga_class,
                'card_type': card_type,
                'lesson_list': lesson_list,
                'active_nav': 'classes',
                'FOR_TRAINING_COURSE': FOR_TRAINING_COURSE
            }
            # NOTE: total_price is price with out promotion
            # NOTE: price is price of one lesson
            if card_type.form_of_using == FOR_TRAINING_COURSE:
                payment_period = None
                if int(enroll_card_form['payment_period']) == 0:
                    total_price = get_price(yoga_class, card_type)
                else:
                    payment_period = yoga_class.payment_periods.all().get(
                        pk=int(enroll_card_form['payment_period']))
                    total_price = payment_period.amount
                context['total_price'] = total_price
                context['payment_period'] = payment_period
            elif card_type.form_of_using == FOR_FULL_MONTH:
                temp_cleaned_data = CardFormForTraineeEnroll(
                    enroll_card_form).cleaned_data
                start_month = temp_cleaned_data['start_at']
                end_month = start_month + relativedelta(months=1)
                number_of_lesson_in_month = yoga_class.lessons.filter(
                    date__range=[start_month, end_month], is_full=False).order_by('date').count()
                price = round(yoga_class.get_price_per_month() /
                              number_of_lesson_in_month / 1000) * 1000
                if lesson_list.count() == number_of_lesson_in_month:
                    total_price = yoga_class.get_price_per_month()
                else:
                    total_price = price * lesson_list.count()
                context['price'] = price
                context['total_price'] = total_price
            else:
                price = get_price(yoga_class, card_type)
                total_price = get_total_price(
                    yoga_class, card_type, lesson_list.count())
                context['price'] = price
                context['total_price'] = total_price
            # PROMOTION
            promotion_type = None
            promotion_code = None
            promotion_val = 'không'
            amount = total_price
            if request.session.get('promotion_code') and request.session.get('promotion_type'):
                # get promotion type
                promotion_type = get_object_or_404(
                    PromotionType, pk=request.session.get('promotion_type'))
                # get promotion code
                promotion_code = get_object_or_404(
                    PromotionCode, pk=request.session.get('promotion_code'))
                value = int(promotion_type.value)
                if promotion_type.category == CASH_PROMOTION:
                    amount -= value
                    promotion_val = '-' + \
                                    sexify.sexy_number(value) + 'đ'
                elif promotion_type.category == PERCENT_PROMOTION:
                    reduce = round(value * amount / 100 / 1000) * 1000
                    amount -= reduce
                    promotion_val = '-' + \
                                    sexify.sexy_number(reduce) + 'đ'
                elif promotion_type.category == FREE_SOME_LESSON_PROMOTION:
                    amount -= value * price
                    promotion_val = '-' + \
                                    sexify.sexy_number(value * price) + 'đ'
                elif promotion_type.category == PLUS_MONTH_PRACTICE_PROMOTION:
                    s = lesson_list.last().date
                    promotion_lessons = yoga_class.lessons.filter(
                        date__gt=s, date__lte=s + relativedelta(months=value), is_full=False).order_by('date')
                    context['promotion_lessons'] = promotion_lessons
                else:
                    promotion_val = promotion_type.full_title
            amount_display = sexify.sexy_number(amount)

            context['promotion_type'] = promotion_type
            context['promotion_code'] = promotion_code
            context['promotion_val'] = promotion_val
            context['amount'] = amount
            context['amount_display'] = amount_display
            return render(request, self.template_name, context=context)
        else:
            messages.error(request, _(
                'You dont have any info to payment. Please try again'))
            return redirect('classes:enroll', slug=slug)

    @transaction.atomic
    def post(self, request, slug):
        yoga_class = YogaClass.objects.get(slug=slug)
        if request.session.get('enroll_card_form') and request.POST.get('payment_type'):
            # enroll_form = CardFormForTraineeEnroll(
            #     request.session['enroll_card_form'])
            if yoga_class.course.course_type == TRAINING_COURSE:
                payment_period_choices = [(0, _('Pay all'))]
                if yoga_class.payment_periods.all().count() > 0:
                    first_payment_period = yoga_class.payment_periods.all().order_by('end_at').first()
                    payment_period_choices.append(
                        (first_payment_period.id, first_payment_period.name), )
                enroll_form = CardFormForTraineeEnroll(
                    request.session['enroll_card_form'], initial={'payment_period_choices': payment_period_choices})
            else:
                enroll_form = CardFormForTraineeEnroll(
                    request.session['enroll_card_form'])
            if request.POST['payment_type'] == 'PREPAID_FREE':
                if enroll_form.is_valid():
                    description = _('Free Registration')
                    charge_id = '0VNDFREE'
                    card = processCard(yoga_class, enroll_form,
                                       request, request.POST['amount'], description, PREPAID, charge_id)
                    request.session['new_card'] = card.pk
                    return redirect('classes:enroll-payment-result', slug=slug)
            elif request.POST['payment_type'] == 'PREPAID_STRIPE':
                card_payment_form = CardPaymentForm(request.POST)
                charge_id = None
                if card_payment_form.is_valid():
                    try:
                        if request.POST.get('stripeToken') and int(request.POST.get('amount')) > 0:
                            # STRIPE CHARGE
                            charge = StripeService(
                                request.POST['name'],
                                request.POST['email'],
                                request.POST['phone'],
                                request.POST['amount'],
                                request.POST['stripeToken'],
                                _('Card Payment')
                            ).call()
                            if charge:
                                charge_id = charge.id
                    except Exception:
                        messages.error(request, _(
                            'An error occurred. Please try again later'))
                        return redirect('classes:enroll-payment', slug=slug)
                if charge_id is None:
                    messages.error(request, _(
                        'An error occurred. Please enter the right number of VisaCard'))
                    return redirect('classes:enroll-payment', slug=slug)
                if enroll_form.is_valid():
                    description = _('Pay card by Stripe')
                    card = processCard(yoga_class, enroll_form,
                                       request, request.POST['amount'], description, PREPAID, charge_id)
                    request.session['new_card'] = card.pk
                    return redirect('classes:enroll-payment-result', slug=slug)
            elif request.POST['payment_type'] == 'POSTPAID':
                if enroll_form.is_valid():
                    description = _('Postpaid')
                    charge_id = None
                    card = processCard(yoga_class, enroll_form,
                                       request, request.POST['amount'], description, POSTPAID, charge_id)
                    request.session['new_card'] = card.pk
                    # NOTES: Add TASK: Remove card after 7 days
                    card_invoice = card.invoices.last()
                    seven_days_after = timezone.now() + timedelta(days=7)
                    removeCardWhenNotPayed.apply_async(args=(card_invoice.pk,), eta=seven_days_after)
                    # RETURN
                    return redirect('classes:postpaid-result', slug=slug)
            else:  # request.POST['payment_type'] == 'PREPAID_MOMO':
                amount = request.POST.get('amount')
                orderId = str(uuid.uuid4())
                requestId = str(uuid.uuid4())
                orderInfo = _('Card Payment')
                returnUrl = request.scheme + '://' + \
                            request.META.get(
                                'HTTP_HOST') + reverse('classes:momo-payment-result', kwargs={'slug': slug})
                notifyUrl = request.scheme + '://' + \
                            request.META.get(
                                'HTTP_HOST') + reverse('classes:momo-payment-result', kwargs={'slug': slug})
                momo = MoMoService(orderInfo, returnUrl,
                                   notifyUrl, amount, orderId, requestId)
                response = momo.call()
                response_data = response.content.decode("utf-8")
                json_response = json.loads(response_data)
                payUrl = json_response['payUrl']
                return redirect(payUrl)
        else:
            messages.error(request, _(
                'An error occurred. Please try again later'))
            return redirect('classes:enroll-payment', slug=slug)

    def __lesson_list_available(self, yoga_class, enroll_card_form):
        cleaned_data = CardFormForTraineeEnroll(enroll_card_form).cleaned_data
        id_arr = eval(cleaned_data['lesson_list'])
        lesson_list = yoga_class.lessons.filter(
            is_full=False, pk__in=id_arr).order_by('date')
        return lesson_list


@method_decorator([login_required], name='dispatch')
class UsePromotionCodeView(View):
    def post(self, request, slug):
        promotion_code = get_object_or_404(
            PromotionCode, value=request.POST['promotion-code'])
        promotion_type = get_object_or_404(
            PromotionType, pk=request.POST['promotion-type']
        )
        request.session['promotion_code'] = promotion_code.pk
        request.session['promotion_type'] = promotion_type.pk
        return redirect('classes:enroll-payment', slug=slug)


@method_decorator([login_required], name='dispatch')
class RemovePromotionCodeView(View):
    def post(self, request, slug):
        if request.session.get('promotion_code'):
            del request.session['promotion_code']
        if request.session.get('promotion_type'):
            del request.session['promotion_type']
        return redirect('classes:enroll-payment', slug=slug)


@method_decorator([login_required], name='dispatch')
class YogaClassPaymentResultView(View):
    template_name = 'payment_result.html'

    def get(self, request, slug):
        if request.session.get('new_card') is not None:
            context = {}
            card = get_object_or_404(Card, pk=request.session.get('new_card'))
            yoga_class = YogaClass.objects.get(slug=slug)
            context['yoga_class'] = yoga_class
            context['paymentType'] = 'Prepaid'
            context['type'] = 'STRIPE_FREE'
            context['card'] = card
            del request.session['new_card']
            return render(request, self.template_name, context=context)
        else:
            return redirect('errors:error-404')


@method_decorator([login_required], name='dispatch')
class YogaClassMoMoPaymentResultView(View):
    template_name = 'payment_result.html'

    def get(self, request, slug):
        if request.GET.get('signature'):
            resonse_signature = MoMoResponseService(
                request.GET['requestId'],
                request.GET['amount'],
                request.GET['orderId'],
                request.GET['orderInfo'],
                request.GET['orderType'],
                request.GET['transId'],
                request.GET['message'],
                request.GET['localMessage'],
                request.GET['responseTime'],
                request.GET['errorCode'],
                request.GET['payType']).signature()
            print("REQUEST GET SIGNATURE", request.GET['signature'])
            print("RESPONSE SIGNATURE", resonse_signature)
            print("COMPARE 2 SIGNATURE",
                  request.GET['signature'] == resonse_signature)
            if request.GET['signature'] != resonse_signature:
                return redirect('errors:error-403')
            context = {}
            yoga_class = YogaClass.objects.get(slug=slug)
            context['yoga_class'] = yoga_class
            context['errorCode'] = int(request.GET['errorCode'])
            context['paymentType'] = 'Prepaid'
            context['type'] = 'MOMO'
            if int(request.GET['errorCode']) == 0:
                if request.session.get('enroll_card_form'):
                    description = _('Momo Payment')
                    #
                    if yoga_class.course.course_type == TRAINING_COURSE:
                        payment_period_choices = [(0, _('Pay all'))]
                        if yoga_class.payment_periods.all().count() > 0:
                            first_payment_period = yoga_class.payment_periods.all().order_by('end_at').first()
                            payment_period_choices.append(
                                (first_payment_period.id, first_payment_period.name), )
                        enroll_form = CardFormForTraineeEnroll(
                            request.session['enroll_card_form'],
                            initial={'payment_period_choices': payment_period_choices})
                    else:
                        enroll_form = CardFormForTraineeEnroll(
                            request.session['enroll_card_form'])
                    #
                    if enroll_form.is_valid():
                        card = processCard(
                            yoga_class, enroll_form, request, request.GET['amount'], description, PREPAID,
                            request.GET['transId'])
                        context['card'] = card
                else:
                    return redirect('errors:error-403')
            return render(request, self.template_name, context=context)
        else:
            return redirect('errors:error-403')


@method_decorator([login_required], name='dispatch')
class YogaClassPostPaidResultView(View):
    template_name = 'payment_result.html'

    def get(self, request, slug):
        if request.session.get('new_card') is not None:
            context = {}
            context['paymentType'] = 'Postpaid'
            card = get_object_or_404(Card, pk=request.session.get('new_card'))
            if card.invoices.last().payment_type != POSTPAID:
                messages.error(request, _(
                    'An error occurred. Please try again later'))
                return redirect('errors:error-403')
            context['card'] = card
            del request.session['new_card']
            return render(request, self.template_name, context=context)
        else:
            return redirect('errors:error-404')


@transaction.atomic
def processCard(yoga_class, enroll_form, request, amount, description, payment_type, charge_id):
    # PROMOTION
    promotion_type = None
    promotion_code = None
    if request.session.get('promotion_code') and request.session.get('promotion_type'):
        promotion_type = get_object_or_404(
            PromotionType, pk=request.session.get('promotion_type'))
        promotion_code = get_object_or_404(
            PromotionCode, pk=request.session.get('promotion_code'))
    # CREATE CARD
    card = create_card(
        yoga_class, enroll_form, request.user.trainee, promotion_code, promotion_type)
    # CREATE CARD INVOICE
    card_invoice = CardInvoiceService(
        card, payment_type, description, amount, charge_id).call()

    # NOTE: ADD PAYMENT PERIOD IF HAVING
    if yoga_class.course.course_type == TRAINING_COURSE:
        if enroll_form.cleaned_data.get('payment_period') is not None:
            if int(enroll_form.cleaned_data.get('payment_period')) != 0:
                payment_period = yoga_class.payment_periods.all().get(
                    pk=enroll_form.cleaned_data.get('payment_period'))
                card_invoice.payment_period = payment_period
                card_invoice.save()

    if promotion_code is not None and promotion_type is not None:
        promotion_code.promotion_type = promotion_type
        promotion_code.save()
        if promotion_type.category == GIFT_PROMOTION:
            # NOTE: Delete quantity in total quantity of product
            for v in promotion_type.promotion_type_products.all():
                product = v.product
                product.quantity -= v.quantity
                if product.quantity <= 0:
                    product.quantity = 0
                product.save()
        card_invoice.apply_promotion_codes.create(
            promotion_code=promotion_code)
    if request.session.get('enroll_card_form'):
        del request.session['enroll_card_form']
    if request.session.get('promotion_code'):
        del request.session['promotion_code']
    if request.session.get('promotion_type'):
        del request.session['promotion_type']
    send_twilio_message(_('Thank you for your register at Yoga Huong Tre'))
    return card


@transaction.atomic
def create_card(yoga_class, enroll_form, trainee, promotion=None, promotion_type=None):
    # TODO: CHECK condition before use Promotion
    id_arr = eval(enroll_form.cleaned_data['lesson_list'])
    if promotion is not None and promotion_type is not None and promotion_type.category == PLUS_MONTH_PRACTICE_PROMOTION:
        temp_lesson_list = yoga_class.lessons.filter(
            is_full=False, pk__in=id_arr).order_by('date')
        month_count = int(promotion_type.value)
        additional_s = temp_lesson_list.last().date
        additional_e = temp_lesson_list.last().date + relativedelta(months=month_count)
        additional_lesson_list = yoga_class.lessons.filter(
            date__gt=additional_s, date__lte=additional_e, is_full=False).order_by('date')
        for l in additional_lesson_list:
            id_arr.append(l.pk)
    lesson_list = yoga_class.lessons.filter(
        is_full=False, pk__in=id_arr).order_by('date')
    card = enroll_form.save(commit=False)
    card.trainee = trainee
    card.yogaclass = yoga_class
    card.save()
    RollCallService(card, lesson_list).call()
    return card

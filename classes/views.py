from common.services.stripe_service import StripeService
import json
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

from courses.models import LEVEL_CHOICES
from classes.models import YogaClass
from courses.models import Course
from core.models import Trainer

from django.db.models import Q
from cards.forms import CardFormForTraineeEnroll

from rest_framework.views import APIView
from rest_framework.response import Response
from lessons.serializers.lesson_serializer import LessonSerializer
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from core.decorators import trainee_required

from django.conf import settings

from rest_framework import status
from django.http import HttpResponse
from common.forms.payment_form import PaymentForm

from card_types.models import (CardType,
                               FOR_FULL_MONTH, FOR_SOME_LESSONS, FOR_TRAINING_COURSE, FOR_TRIAL)

from common.templatetags import sexify
from classes.utils import get_price, get_total_price, get_total_price_display
from django.db import transaction
from common.services.card_invoice_service import CardInvoiceService
from common.services.roll_call_service import RollCallService
from django.contrib import messages
from classes.forms import FilterForm
from django.db.models import Value as V
from django.db.models.functions import Concat
from promotions.models import PromotionCode, Promotion, PromotionType, CASH_PROMOTION, PERCENT_PROMOTION


class YogaClassListView(ListView):
    model = YogaClass
    template_name = 'classes/list.html'
    context_object_name = 'classes'
    ordering = ['created_at']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        query_course = list(((None, 'Chọn khóa học'),)) + \
            list(Course.objects.values_list('slug', 'name'))
        query_trainer = list(((None, 'Chọn huấn luyện viên'),)) + list(Trainer.objects.annotate(
            full_name=Concat('user__first_name', V(' '), 'user__last_name')).values_list('user__slug', 'full_name'))

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
        queryset = YogaClass.objects.filter(**filter_options)
        return queryset


class YogaClassDetailView(DetailView):
    model = YogaClass
    template_name = 'classes/show.html'
    slug_field = 'slug'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super(YogaClassDetailView, self).get_context_data(**kwargs)
        context['active_nav'] = 'classes'
        context['others'] = set(
            YogaClass.objects.filter(~Q(pk=self.object.pk)))
        return context


@method_decorator([login_required, trainee_required], name='dispatch')
class YogaClassEnrollView(View):
    template_name = 'classes/enroll.html'

    def get(self, request, slug):
        yoga_class = YogaClass.objects.get(slug=slug)
        if self.__is_trainee_of_class(yoga_class, request.user.trainee):
            messages.success(
                request,
                _('Your card is still in use. Please choose extend card only'))
            return redirect('classes:detail', slug=slug)
        # remove enroll card form when access enroll page
        if request.session.get('enroll_card_form') is not None:
            del request.session['enroll_card_form']
        card_type_list = yoga_class.course.card_types.all()
        form = CardFormForTraineeEnroll(
            initial={'card_type_list': card_type_list})
        context = {
            'yoga_class': yoga_class,
            'form': form,
            'active_nav': 'classes'
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        yoga_class = YogaClass.objects.get(slug=kwargs['slug'])
        form = CardFormForTraineeEnroll(
            request.POST, initial={'yoga_class': yoga_class})

        if form.is_valid():
            # save to session and get it in payment page
            request.session['enroll_card_form'] = request.POST
            return HttpResponse({'success': 'success'}, status=status.HTTP_200_OK)
        return HttpResponse(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)

    def __is_trainee_of_class(self, yoga_class, trainee):
        cards = yoga_class.cards.filter(trainee=trainee)
        if cards:
            card = cards.last()
            if card.lessons.last().date >= datetime.now().date():
                return True
        return False


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
            lesson_list = self.__lesson_list_available(
                yoga_class, enroll_card_form)
            # Payment Form
            form = PaymentForm()
            id_card_type = enroll_card_form['card_type']
            card_type = CardType.objects.get(pk=id_card_type)

            start_at = lesson_list.first().date
            end_at = lesson_list.last().date
            number_of_lessons = lesson_list.count()
            price = get_price(yoga_class, card_type)
            total_price = get_total_price(
                yoga_class, card_type, number_of_lessons)
            total_price_display = get_total_price_display(total_price)
            # promotion
            promotion_type = None
            promotion_code = None
            promotion_val = 'không'
            amount = total_price
            if request.session.get('promotion_code') and request.session.get('promotion_type'):
                promotion_type = get_object_or_404(
                    PromotionType, pk=request.session.get('promotion_type'))
                promotion_code = get_object_or_404(
                    PromotionCode, pk=request.session.get('promotion_code'))
                if promotion_type.category == CASH_PROMOTION:
                    amount -= promotion_type.value
                    promotion_val = '-' + \
                        sexify.sexy_number(promotion_type.value) + 'đ'
                elif promotion_type.category == PERCENT_PROMOTION:
                    amount -= promotion_type.value*amount
                    promotion_val = '-' + \
                        sexify.sexy_number(promotion_type.value*amount) + 'đ'
                else:
                    promotion_val = promotion_type.full_title()
            amount_display = sexify.sexy_number(amount)

            context = {
                'key': settings.STRIPE_PUBLISHABLE_KEY,
                'form': form,
                'yoga_class': yoga_class,
                'card_type': card_type,
                'start_at': start_at,
                'end_at': end_at,
                'number_of_lessons': number_of_lessons,
                'lesson_list': lesson_list,
                'price': price,
                'total_price_display': total_price_display,
                'total_price': total_price,
                'active_nav': 'classes',
                'promotion_type': promotion_type,
                'promotion_code': promotion_code,
                'promotion_val': promotion_val,
                'amount': amount,
                'amount_display': amount_display
            }
            return render(request, self.template_name, context=context)
        else:
            return redirect('classes:enroll', slug=slug)

    @transaction.atomic
    def post(self, request, slug):
        if request.session.get('enroll_card_form'):
            card_payment_form = PaymentForm(request.POST)
            description = self.__description(
                request.POST['name'], request.POST['email'], request.POST['amount'])
            if card_payment_form.is_valid():
                try:
                    yoga_class = YogaClass.objects.get(slug=slug)
                    enroll_form = CardFormForTraineeEnroll(
                        request.session['enroll_card_form'])
                    if request.POST.get('stripeToken') and float(request.POST.get('amount')) > 0:
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
                            if enroll_form.is_valid():
                                # CREATE CARD
                                card = self.__create_card(
                                    yoga_class, enroll_form, request.user.trainee)
                                # CREATE CARD INVOICE
                                card_invoice = CardInvoiceService(
                                    card, description, request.POST['amount'], charge.id).call()
                                # ADD PROMOTION TO CARD INVOICE
                    else:
                        # CREATE CARD
                        card = self.__create_card(
                            yoga_class, enroll_form, request.user.trainee)
                        # CREATE CARD INVOICE
                        card_invoice = CardInvoiceService(
                            card, description, request.POST['amount']).call()
                    del request.session['enroll_card_form']
                    return HttpResponse('success', status=status.HTTP_200_OK)
                except Exception as e:
                    print("<ERROR>")
                    print(e)
                    return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

            else:
                return HttpResponse(card_payment_form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = {}
            response_data['message'] = _(
                'Please enroll a class before payment')
            return HttpResponse(json.dumps(response_data), status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def __create_card(self, yoga_class, enroll_form, trainee):
        start = enroll_form.cleaned_data['start_at']
        end = enroll_form.cleaned_data['end_at']
        lesson_list = yoga_class.lessons.filter(
            date__range=[start, end])
        card = enroll_form.save(commit=False)
        card.trainee = trainee
        card.yogaclass = yoga_class
        card.save()
        RollCallService(card, lesson_list).call()
        return card

    def __description(self, name, email, amount):
        listStr = [name, _('with'), _('email'), email, _('paied'), str(amount)]
        result = ' '.join(listStr)
        return result

    def __lesson_list_available(self, yoga_class, enroll_card_form):
        cleaned_data = CardFormForTraineeEnroll(enroll_card_form).cleaned_data
        start = cleaned_data['start_at']
        end = cleaned_data['end_at']
        lesson_list = yoga_class.lessons.filter(
            date__range=[start, end], is_full=False).order_by('date')
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

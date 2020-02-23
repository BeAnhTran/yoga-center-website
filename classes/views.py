from common.services.stripe_service import StripeService
import json
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

from classes.models import YogaClass, LEVEL_CHOICES
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
import stripe

from rest_framework import status
from django.http import HttpResponse
from cards.forms import CardPaymentForm

from card_types.models import (CardType,
                               FOR_FULL_MONTH, FOR_SOME_LESSONS, FOR_TRAINING_COURSE, FOR_TRIAL)

from common.templatetags import sexify
from classes.utils import get_price, get_total_price, get_total_price_display
from django.db import transaction
from common.services.card_invoice_service import CardInvoiceService

class YogaClassListView(ListView):
    model = YogaClass
    template_name = 'classes/list.html'
    context_object_name = 'classes'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(YogaClassListView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['levels'] = LEVEL_CHOICES
        context['trainers'] = Trainer.objects.all()
        return context


class YogaClassDetailView(DetailView):
    model = YogaClass
    template_name = 'classes/show.html'
    slug_field = 'slug'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super(YogaClassDetailView, self).get_context_data(**kwargs)
        context['others'] = set(
            YogaClass.objects.filter(~Q(pk=self.object.pk)))
        return context


@method_decorator([login_required, trainee_required], name='dispatch')
class YogaClassEnrollView(View):
    template_name = 'classes/enroll.html'

    def get(self, request, slug):
        yoga_class = YogaClass.objects.get(slug=slug)
        if self.__is_trainee_of_class(yoga_class, request.user.trainee):
            return redirect('classes:detail',slug=slug)
        # remove enroll card form when access enroll page
        if request.session.get('enroll_card_form') is not None:
            del request.session['enroll_card_form']
        card_type_list = yoga_class.card_types.all()
        form = CardFormForTraineeEnroll(
            initial={'card_type_list': card_type_list})
        context = {
            'yoga_class': yoga_class,
            'form': form
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
            if card.lessons.last().day >= datetime.now().date():
                return True
        return False


class YogaClassGetLessonListView(APIView):
    # Get List Lesson for specified Yoga Class in range time
    def get(self, request, slug):
        obj = YogaClass.objects.get(slug=slug)
        start_date = datetime.fromisoformat(request.GET['startStr'])
        end_date = datetime.fromisoformat(request.GET['endStr'])
        lessons = obj.lessons.filter(day__range=[start_date, end_date])
        serialized = LessonSerializer(lessons, many=True)
        return Response(serialized.data)


@method_decorator([login_required, trainee_required], name='dispatch')
class YogaClassEnrollPaymentView(View):
    template_name = 'payment.html'

    def get(self, request, slug):
        if request.session.get('enroll_card_form'):
            yoga_class = YogaClass.objects.get(slug=slug)
            enroll_card_form = request.session['enroll_card_form']
            lesson_list = self.__lesson_list(yoga_class, enroll_card_form)
            # Payment Form
            form = CardPaymentForm()
            id_card_type = enroll_card_form['card_type']
            card_type = CardType.objects.get(pk=id_card_type)

            start_at = lesson_list.first().day
            end_at = lesson_list.last().day
            number_of_lessons = lesson_list.count()
            price = get_price(yoga_class, card_type)
            total_price = get_total_price(
                yoga_class, card_type, number_of_lessons)
            total_price_display = get_total_price_display(total_price)

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
                'total_price': total_price
            }
            return render(request, self.template_name, context=context)
        else:
            return redirect('classes:enroll',slug=slug)

    @transaction.atomic
    def post(self, request, slug):
        if request.session.get('enroll_card_form'):
            card_payment_form = CardPaymentForm(request.POST)
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
                                CardInvoiceService(
                                    card, description, request.POST['amount'], charge.id).call()
                    else:
                        # CREATE CARD
                        card = self.__create_card(
                            yoga_class, enroll_form, request.user.trainee)
                        # CREATE CARD INVOICE
                        CardInvoiceService(
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
            day__range=[start, end])
        card = enroll_form.save(commit=False)
        card.trainee = trainee
        card.yogaclass = yoga_class
        card.save()
        card.lessons.add(*lesson_list)
        return card

    def __description(self, name, email, amount):
        listStr = [name, _('with'), _('email'), email, _('paied'), str(amount)]
        result = ' '.join(listStr)
        return result

    def __lesson_list(self, yoga_class, enroll_card_form):
        cleaned_data = CardFormForTraineeEnroll(enroll_card_form).cleaned_data
        start = cleaned_data['start_at']
        end = cleaned_data['end_at']
        lesson_list = yoga_class.lessons.filter(
            day__range=[start, end]).order_by('day')
        return lesson_list

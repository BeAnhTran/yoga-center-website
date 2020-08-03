from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views import View
from services.sms_service import send_twilio_message
from services.stripe_service import StripeService
from django.conf import settings
from django.db import transaction
from apps.donations import forms
from apps.donations.models import Donation
from django.http import HttpResponse
from rest_framework import status
import json


class IndexView(View):
    template_name = 'donations/index.html'

    def get(self, request):
        form = forms.DonationForm()
        context = {
            'form': form,
            'key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, self.template_name, context=context)

    @transaction.atomic
    def post(self, request):
        donate_form = forms.DonationForm(request.POST)
        if donate_form.is_valid():
            try:
                if request.POST.get('stripeToken') and int(request.POST.get('amount')) > 0:
                    # STRIPE CHARGE
                    charge = StripeService(
                        request.POST['name'],
                        request.POST['email'],
                        request.POST['phone'],
                        request.POST['amount'],
                        request.POST['stripeToken'],
                        _('Donate')
                    ).call()
                    if charge:
                        charge_id = charge.id
                        Donation.objects.create(**{
                            'name': request.POST['name'],
                            'email': request.POST['email'],
                            'phone_number': request.POST['phone'],
                            'content': request.POST['content'],
                            'amount': request.POST['amount'],
                            'charge_id': charge_id
                        })
                        send_twilio_message(
                            _('Thank you for your donation to HT Yoga'))
                        return HttpResponse('success', status=status.HTTP_200_OK)
            except Exception as e:
                print("<ERROR>")
                print(e)
                return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(donate_form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)

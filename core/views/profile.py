from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from core.forms.profile_forms import UsernameEmailForm, BasicInfoForm, AdditionalInfoForm, HealthConditionForm
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from core.decorators import trainee_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from core.serializers.trainee_serializers import TraineeSerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.db import transaction
from cards.models import Card


@method_decorator([login_required], name='dispatch')
class ProfileView(View):
    template_name = 'profile/index.html'

    def get(self, request):
        form1 = UsernameEmailForm(instance=request.user)
        form1.fields['hidden_field'].initial = 'username_email'
        form_basic_info = BasicInfoForm(instance=request.user)
        form_basic_info.fields['hidden_field'].initial = 'basic_info'
        form_additional_info = AdditionalInfoForm(instance=request.user)
        form_additional_info.fields['hidden_field'].initial = 'additional_info'
        context = {}
        context['form1'] = form1
        context['form_basic_info'] = form_basic_info
        context['form_additional_info'] = form_additional_info
        if request.user.is_trainee:
            form_health_condition = HealthConditionForm(
                instance=request.user.trainee)
            context['form_health_condition'] = form_health_condition

        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        if request.POST.get('hidden_field') is not None and request.POST.get('hidden_field') == 'username_email':
            form1 = UsernameEmailForm(request.POST, instance=request.user)
            if form1.is_valid():
                form1.save()
                messages.success(request, _('Update successfully'))
                return redirect('core:profile')
        else:
            form1 = UsernameEmailForm(instance=request.user)
            form1.fields['hidden_field'].initial = 'username_email'

        if request.POST.get('hidden_field') is not None and request.POST.get('hidden_field') == 'basic_info':
            form_basic_info = BasicInfoForm(
                request.POST, instance=request.user)
            if form_basic_info.is_valid():
                form_basic_info.save()
                messages.success(request, _('Update successfully'))
                return redirect('core:profile')
        else:
            form_basic_info = BasicInfoForm(instance=request.user)
            form_basic_info.fields['hidden_field'].initial = 'basic_info'

        if request.POST.get('hidden_field') is not None and request.POST.get('hidden_field') == 'additional_info':
            form_additional_info = AdditionalInfoForm(
                request.POST, instance=request.user)
            if form_additional_info.is_valid():
                form_additional_info.save()
                messages.success(request, _('Update successfully'))
                return redirect('core:profile')
        else:
            form_additional_info = AdditionalInfoForm(instance=request.user)
            form_additional_info.fields['hidden_field'].initial = 'additional_info'

        context = {
            'form1': form1,
            'form_basic_info': form_basic_info,
            'form_additional_info': form_additional_info
        }
        return render(request, self.template_name, context=context)


@login_required
@trainee_required
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@transaction.atomic
def update_health_condition(request):
    form = HealthConditionForm(request.POST, instance=request.user.trainee)
    if form.is_valid():
        trainee = form.save()
        messages.success(request, _('Update successfully'))
        serialized = TraineeSerializer(trainee)
        return Response(serialized.data)
    return HttpResponse(form.errors.as_json(), status=400)


@method_decorator([login_required, trainee_required], name='dispatch')
class TraineeCardsView(View):
    template_name = 'profile/trainees/cards.html'

    def get(self, request):
        context = {}
        cards = request.user.trainee.cards.all()
        context['cards'] = cards
        return render(request, self.template_name, context=context)


@method_decorator([login_required, trainee_required], name='dispatch')
class TraineeCardExtendView(View):
    template_name = 'profile/trainees/card_extend.html'

    def get(self, request, pk):
        card = Card.objects.get(pk=pk)
        context = {}
        context['card'] = card
        return render(request, self.template_name, context=context)

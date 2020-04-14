from django.shortcuts import redirect, render, reverse
from django.views.generic import TemplateView
from apps.core.forms.profile_forms import UsernameEmailForm, BasicInfoForm, AdditionalInfoForm, HealthConditionForm
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from apps.core.decorators import trainee_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from apps.core.serializers.trainee_serializers import TraineeSerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.db import transaction
from apps.cards.models import Card
from apps.cards.forms import ExtendCardRequestForm
from apps.core.forms.certificate_forms import CertificateForm


@method_decorator([login_required], name='dispatch')
class ProfileView(View):
    template_name = 'profile/index.html'

    def get(self, request):
        form1 = UsernameEmailForm(instance=request.user)
        form1.fields['hidden_field'].initial = 'username_email'
        # Basic Info Form
        form_basic_info = BasicInfoForm(instance=request.user)
        form_basic_info.fields['hidden_field'].initial = 'basic_info'
        # Additional Info Form
        form_additional_info = AdditionalInfoForm(instance=request.user)
        form_additional_info.fields['hidden_field'].initial = 'additional_info'
        context = {}
        context['form1'] = form1
        context['form_basic_info'] = form_basic_info
        context['form_additional_info'] = form_additional_info
        context['sidebar_profile'] = 'info'

        # Health Condition Form (Trainee)
        if request.user.is_trainee:
            form_health_condition = HealthConditionForm(
                instance=request.user.trainee)
            context['form_health_condition'] = form_health_condition

        # Certificate Form (Trainer | Staff)
        if request.user.is_trainer or request.user.is_staff:
            form_certificate = CertificateForm()
            form_certificate.fields['hidden_field'].initial = 'certificate'
            context['form_certificate'] = form_certificate
            # assign certificate_user_obj (Trainer or Staff)
            if request.user.is_trainer:
                certificate_user_obj = request.user.trainer
            else:
                certificate_user_obj = request.user.staff
            context['certificate_user_obj'] = certificate_user_obj

        # Focus and scroll
        if request.GET.get('focus'):
            context['focus'] = request.GET['focus']
        else:
            context['focus'] = ''

        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        context = {}
        context['focus'] = ''
        # Email Form
        if request.POST.get('hidden_field') is not None and request.POST.get('hidden_field') == 'username_email':
            form1 = UsernameEmailForm(request.POST, instance=request.user)
            if form1.is_valid():
                form1.save()
                messages.success(request, _('Update successfully'))
                return redirect('core:profile')
        else:
            form1 = UsernameEmailForm(instance=request.user)
            form1.fields['hidden_field'].initial = 'username_email'
            context['form1'] = form1

        # Basic Info Form
        if request.POST.get('hidden_field') is not None and request.POST.get('hidden_field') == 'basic_info':
            form_basic_info = BasicInfoForm(
                request.POST, instance=request.user)
            if form_basic_info.is_valid():
                form_basic_info.save()
                messages.success(request, _('Update successfully'))
                return redirect(reverse('core:profile') + '?focus=collapseBasicInfo')
        else:
            form_basic_info = BasicInfoForm(instance=request.user)
            form_basic_info.fields['hidden_field'].initial = 'basic_info'
            context['form_basic_info'] = form_basic_info
            context['focus'] = 'collapseBasicInfo'

        # Additional Info Form
        if request.POST.get('hidden_field') is not None and request.POST.get('hidden_field') == 'additional_info':
            form_additional_info = AdditionalInfoForm(
                request.POST, instance=request.user)
            if form_additional_info.is_valid():
                form_additional_info.save()
                messages.success(request, _('Update successfully'))
                return redirect(reverse('core:profile') + '?focus=collapseAdditionalInfo')
        else:
            form_additional_info = AdditionalInfoForm(instance=request.user)
            form_additional_info.fields['hidden_field'].initial = 'additional_info'
            context['form_additional_info'] = form_additional_info
            context['focus'] = 'collapseAdditionalInfo'

        # Certificate Form
        if request.POST.get('hidden_field') is not None and request.POST.get('hidden_field') == 'certificate':
            form_certificate = CertificateForm(request.POST, request.FILES)
            if form_certificate.is_valid():
                # remove hidden field
                form_certificate.cleaned_data.pop('hidden_field')
                if request.user.is_trainer:
                    user_obj = request.user.trainer
                else:
                    user_obj = request.user.staff
                user_obj.certificates.create(**form_certificate.cleaned_data)

                messages.success(request, _('Create certificate successfully'))
                return redirect(reverse('core:profile') + '?focus=collapseCertificate')
        else:
            form_certificate = CertificateForm()
            form_certificate.fields['hidden_field'].initial = 'certificate'
            context['form_certificate'] = form_certificate
            context['focus'] = 'collapseCertificate'

        # Active Sidebar
        context['sidebar_profile'] = 'info'
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

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from apps.certificates.models import Certificate


@method_decorator([login_required], name='dispatch')
class ProfileCerfiticateView(View):
    template_name = 'profile/certificates/list.html'

    def get(self, request):
        context = {}
        certificates = request.user.certificates.all()
        context['certificates'] = certificates
        context['sidebar_profile'] = 'certificates'
        return render(request, self.template_name, context=context)


@method_decorator([login_required], name='dispatch')
class ProfileCertificateDetailView(DetailView):
    model = Certificate
    template_name = 'profile/certificates/detail.html'
    context_object_name = 'certificate'

    def get_context_data(self, **kwargs):
        context = super(ProfileCertificateDetailView, self).get_context_data(**kwargs)
        context['sidebar_profile'] = 'certificates'
        return context

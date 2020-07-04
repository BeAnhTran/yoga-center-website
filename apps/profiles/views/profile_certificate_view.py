from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView


@method_decorator([login_required], name='dispatch')
class ProfileCerfiticateView(View):
    template_name = 'profile/certificates/list.html'

    def get(self, request):
        context = {}
        certificates = request.user.certificates.all()
        context['certificates'] = certificates
        context['sidebar_profile'] = 'certificates'
        return render(request, self.template_name, context=context)

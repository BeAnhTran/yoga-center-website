from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from apps.certificates.models import Certificate
from apps.profiles.forms import certificate_form
from django.db import transaction
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


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
        context = super(ProfileCertificateDetailView,
                        self).get_context_data(**kwargs)
        context['sidebar_profile'] = 'certificates'
        return context


@method_decorator([login_required], name='dispatch')
class ProfileCertificateNewView(View):
    template_name = 'profile/certificates/new.html'

    def get(self, request):
        form = certificate_form.CertificateForm()
        context = {
            'sidebar_profile': 'certificates',
            'form': form
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        form = certificate_form.CertificateForm(request.POST, request.FILES)
        context = {
            'form': form,
            'sidebar_profile': 'certificates'
        }

        if form.is_valid():
            request.user.certificates.create(
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                image=form.cleaned_data.get('image'),
            )
            messages.success(request, 'Thêm chứng nhận mới thành công')
            return redirect('profile:certificates')

        messages.error(request, 'Đã có lỗi xảy ra. Vui lòng thử lại.')
        return render(request, self.template_name, context=context)


@method_decorator([login_required], name='dispatch')
class ProfileCertificateEditView(View):
    template_name = 'profile/certificates/edit.html'

    def get(self, request, pk):
        certificate = get_object_or_404(Certificate, pk=pk)
        form = certificate_form.CertificateForm(instance=certificate)
        context = {
            'sidebar_profile': 'certificates',
            'form': form,
            'certificate': certificate
        }
        return render(request, self.template_name, context=context)

    def post(self, request, pk, **kwargs):
        certificate = get_object_or_404(Certificate, pk=pk)
        form = certificate_form.CertificateForm(request.POST, request.FILES)
        context = {
            'form': form,
            'sidebar_profile': 'certificates',
            'certificate': certificate
        }

        if form.is_valid():
            certificate.name = form.cleaned_data.get('name')
            certificate.description = form.cleaned_data.get('description')
            if 'image' in form.changed_data:
                certificate.image = form.cleaned_data.get('image')
            certificate.save()
            messages.success(request, 'Chỉnh sửa chứng nhận thành công')
            return redirect('profile:certificates')

        messages.error(request, 'Đã có lỗi xảy ra. Vui lòng thử lại.')
        return render(request, self.template_name, context=context)


@method_decorator([login_required], name='dispatch')
class CertificateDeleteView(DeleteView):
    model = Certificate
    success_url = reverse_lazy('profile:certificates')
    success_message = "Xóa chứng nhận thành công."

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(CertificateDeleteView, self).delete(request, *args, **kwargs)

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.utils.decorators import method_decorator
from ..decorators import admin_required
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from apps.dashboard.forms.faq_form import FAQForm
from apps.faq.models import FAQ
from django.db import transaction


@method_decorator([login_required, admin_required], name='dispatch')
class FAQListView(ListView):
    model = FAQ
    template_name = 'dashboard/faq/list.html'
    context_object_name = 'faqs'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(FAQListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'faq'
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class FAQNewView(View):
    template_name = 'dashboard/faq/new.html'

    def get(self, request):
        form = FAQForm()
        context = {
            'form': form,
            'active_nav': 'faq'
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = FAQForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('dashboard:faq-list')

        context = {
            'form': form,
            'active_nav': 'faq'
        }
        return render(request, self.template_name, context=context)


@method_decorator([login_required, admin_required], name='dispatch')
class FAQEditView(UpdateView):
    model = FAQ
    template_name = 'dashboard/faq/edit.html'
    form_class = FAQForm

    def get_success_url(self):
        return reverse('dashboard:faq-list', kwargs={})


@method_decorator([login_required, admin_required], name='dispatch')
class FAQDeleteView(DeleteView):
    model = FAQ
    success_url = reverse_lazy('dashboard:faq-list')

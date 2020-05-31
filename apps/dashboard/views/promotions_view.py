from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from ..decorators import admin_required, staff_required
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.promotions.models import Promotion
from apps.dashboard.forms import promotions_form


@method_decorator([login_required, staff_required], name='dispatch')
class PromotionListView(ListView):
    model = Promotion
    template_name = 'dashboard/promotions/list.html'
    context_object_name = 'promotions'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PromotionListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'promotions'
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class PromotionNewView(View):
    template_name = 'dashboard/promotions/new.html'

    def get(self, request):
        form = promotions_form.PromotionForm()
        context = {
            'form': form,
            'active_nav': 'promotions'
        }
        if self.request.POST:
            context['promotion_types'] = promotions_form.PromotionTypeFormSet(
                self.request.POST)
        else:
            context['promotion_types'] = promotions_form.PromotionTypeFormSet()

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = promotions_form.PromotionForm(request.POST, request.FILES)
        promotion_types = promotions_form.PromotionTypeFormSet(request.POST)

        with transaction.atomic():
            if form.is_valid():
                obj = form.save()
                if promotion_types.is_valid():
                    promotion_types.instance = obj
                    promotion_types.save()

                return redirect('dashboard:promotions-list')

        context = {
            'form': form,
            'promotion_types': promotion_types
        }
        return render(request, self.template_name, context=context)


@method_decorator([login_required, staff_required], name='dispatch')
class PromotionDetailView(DetailView):
    model = Promotion
    template_name = 'dashboard/promotions/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PromotionDetailView, self).get_context_data(**kwargs)
        context['active_nav'] = 'promotions'
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class PromotionEditView(UpdateView):
    model = Promotion
    template_name = 'dashboard/promotions/edit.html'
    form_class = promotions_form.PromotionEditForm

    def get_success_url(self):
            return reverse('dashboard:promotions-list', kwargs={})

    def get_context_data(self, **kwargs):
        context = super(PromotionEditView, self).get_context_data(**kwargs)
        context['active_nav'] = 'promotions'
        if self.request.POST:
            context['promotion_types'] = promotions_form.PromotionTypeFormSet(
                self.request.POST, instance=self.object)
        else:
            context['promotion_types'] = promotions_form.PromotionTypeFormSet(
                instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        promotion_types = context['promotion_types']
        with transaction.atomic():
            self.object = form.save()
            if promotion_types.is_valid():
                promotion_types.instance = self.object
                promotion_types.save()
        return super(PromotionEditView, self).form_valid(form)


@method_decorator([login_required, admin_required], name='dispatch')
class PromotionDeleteView(DeleteView):
    model = Promotion
    success_url = reverse_lazy('dashboard:promotions-list')


@method_decorator([login_required, admin_required], name='dispatch')
class PromotionCodeListView(View):
    template_name = 'dashboard/promotions/codes/list.html'

    def get(self, request, pk):
        promotion = get_object_or_404(Promotion, pk=pk)
        codes = promotion.codes.all()
        context = {
            'promotion': promotion,
            'codes': codes,
            'active_nav': 'promotions'
        }

        return render(request, self.template_name, context=context)


@login_required
@admin_required
def createPromotionCode(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    promotion.codes.create()
    return redirect('dashboard:promotions-codes-list', promotion.pk)

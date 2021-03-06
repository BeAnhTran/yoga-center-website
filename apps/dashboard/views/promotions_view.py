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
from apps.promotions.models import Promotion, GIFT_PROMOTION
from apps.dashboard.forms import promotions_form
from apps.shop.models import Product


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
                    product_promotion_types = obj.promotion_types.filter(
                        category=GIFT_PROMOTION)
                    if product_promotion_types.count() > 0 and request.POST.get('index-gift-type') is not None:
                        product_promotion_type = product_promotion_types.first()
                        idx = request.POST.get('index-gift-type')
                        c = request.POST.get(
                            'promotion_types-' + idx + '-value')
                        count = 0
                        for x in range(int(c)):
                            temp_product = 'promotion_types-' + \
                                str(idx) + '-product-' + str(x)
                            temp_quantity = 'promotion_types-' + \
                                str(idx) + '-quantity-' + str(x)
                            if int(request.POST[temp_product]) > 0:
                                p = Product.objects.get(
                                    pk=int(request.POST[temp_product]))
                                product_promotion_type.promotion_type_products.create(
                                    product=p, quantity=request.POST[temp_quantity])
                                count += 1
                        product_promotion_type.value = count
                        product_promotion_type.save()
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

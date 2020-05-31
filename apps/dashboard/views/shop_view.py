from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views import View

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required

from apps.shop.models import Product, ProductCategory, Bill
from apps.dashboard.forms import product_categories_form, products_form


#******************
# PRODUCT CATEGORY
#******************


@method_decorator([login_required, staff_required], name='dispatch')
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'dashboard/shop/categories/list.html'
    context_object_name = 'categories'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryListView,
                        self).get_context_data(**kwargs)
        context['active_nav'] = 'product_categories'
        context['show_nav_shop'] = True
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class ProductCategoryNewView(View):
    template_name = 'dashboard/shop/categories/new.html'

    def get(self, request):
        form = product_categories_form.ProductCategoryForm()
        context = {
            'form': form,
            'active_nav': 'product_categories',
            'show_nav_shop': True
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        form = product_categories_form.ProductCategoryForm(
            request.POST, request.FILES)
        context = {
            'form': form,
            'active_nav': 'product_categories',
            'show_nav_shop': True
        }

        if form.is_valid():
            form.save()
            return redirect('dashboard:shop-categories-list')

        return render(request, self.template_name, context=context)


@method_decorator([login_required, staff_required], name='dispatch')
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('dashboard:shop-categories-list')


#******************
# PRODUCT
#******************


@method_decorator([login_required, staff_required], name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'dashboard/shop/products/list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProductListView,
                        self).get_context_data(**kwargs)
        context['active_nav'] = 'products'
        context['show_nav_shop'] = True
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class ProductNewView(View):
    template_name = 'dashboard/shop/products/new.html'

    def get(self, request):
        form = products_form.ProductForm()
        context = {
            'form': form,
            'active_nav': 'products',
            'show_nav_shop': True
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        form = products_form.ProductForm(request.POST, request.FILES)
        context = {
            'form': form,
            'active_nav': 'products',
            'show_nav_shop': True
        }

        if form.is_valid():
            form.save()
            return redirect('dashboard:shop-products-list')

        return render(request, self.template_name, context=context)


#******************
# BILLS
#******************

@method_decorator([login_required, staff_required], name='dispatch')
class BillListView(ListView):
    model = Bill
    template_name = 'dashboard/shop/bills.html'
    context_object_name = 'bills'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(BillListView,
                        self).get_context_data(**kwargs)
        context['active_nav'] = 'bills'
        context['show_nav_shop'] = True
        return context

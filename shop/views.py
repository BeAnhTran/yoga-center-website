from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404

from shop.models import Product, ProductCategory


class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 4
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        product_categories = ProductCategory.objects.all()
        context['product_categories'] = product_categories
        context['active_nav'] = 'shop'
        return context

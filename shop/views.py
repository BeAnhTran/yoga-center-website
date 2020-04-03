from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404

from shop.models import Product, ProductCategory
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product_categories = ProductCategory.objects.all()
        context['product_categories'] = product_categories
        context['active_nav'] = 'shop'
        return context


class AddToCartApiView(APIView):
    def post(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        quantity = 1
        if request.POST.get('quantity') is not None:
            quantity = int(request.POST.get('quantity'))

        if request.session.get('cart') is not None:
            if request.session['cart'].get(str(pk)) is not None:
                request.session['cart'][str(pk)]['quantity'] += quantity
            else:
                request.session['cart'][str(pk)]['quantity'] = quantity
        else:
            request.session['cart'] = {}
            request.session['cart'][str(pk)] = {
                'slug': product.slug,
                'quantity': quantity
            }
        return Response('Đã thêm vào giỏ hàng', status=status.HTTP_200_OK)

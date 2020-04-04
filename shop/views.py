from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404

from shop.models import Product, ProductCategory
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from common.forms.payment_form import PaymentForm
from django.conf import settings


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
                request.session['cart'][str(pk)] = {
                    'slug': product.slug,
                    'quantity': quantity
                }
        else:
            request.session['cart'] = {}
            request.session['cart'][str(pk)] = {
                'slug': product.slug,
                'quantity': quantity
            }
        return Response('Đã thêm vào giỏ hàng', status=status.HTTP_200_OK)


class ChangeProductCartQuantityApiView(APIView):
    def post(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        if product:
            if request.POST.get('quantity') is not None:
                quantity = int(request.POST.get('quantity'))
            else:
                quantity = 1
            request.session['cart'][str(pk)]['quantity'] = quantity
            return Response('Đã thay đổi số sản phẩm trong giỏ hàng', status=status.HTTP_200_OK)


class RemoveProductOutOfCartView(View):
    def post(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        if product:
            del request.session['cart'][str(pk)]
            return redirect('shop:cart')


class CartView(View):
    template_name = 'shop/cart.html'

    def get(self, request):
        context = {}
        context['cart'] = []
        if request.session.get('cart'):
            cart = request.session.get('cart')
            for product_id in cart:
                product = get_object_or_404(Product, pk=product_id)
                context['cart'].append({
                    'product': product,
                    'quantity': cart[str(product_id)]['quantity']
                })
        else:
            context['cart'] = None
        return render(request, self.template_name, context=context)


@method_decorator([login_required], name='dispatch')
class CheckOutView(View):
    template_name = 'shop/checkout.html'

    def get(self, request):
        context = {}
        # Payment Form
        payment_form = PaymentForm()
        context['payment_form'] = payment_form
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY

        context['cart'] = []
        total = 0
        if request.session.get('cart'):
            cart = request.session.get('cart')
            for product_id in cart:
                product = get_object_or_404(Product, pk=product_id)
                sub_total = product.price * cart[str(product_id)]['quantity']
                total += sub_total
                context['cart'].append({
                    'product': product,
                    'quantity': cart[str(product_id)]['quantity'],
                    'sub_total': sub_total
                })
        else:
            context['cart'] = None
        context['total'] = total
        return render(request, self.template_name, context=context)

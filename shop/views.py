from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib import messages
import json

from shop.models import Product, ProductCategory
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from common.forms.payment_form import PaymentForm
from django.conf import settings
from django.db import transaction
from common.services.stripe_service import StripeService
from common.services.bill_service import BillService
from django.utils.translation import gettext as _

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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
        response_data = {
            'message': 'Đã thêm vào giỏ hàng',
            'products_count': request.session['cart'].__len__()
        }
        return Response(json.dumps(response_data), status=status.HTTP_200_OK)


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

    @transaction.atomic
    def post(self, request):
        context = {}
        context['cart'] = None
        total = 0
        amount = 0
        promotion = 0
        if request.session.get('cart'):
            context['cart'] = []
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

        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            try:
                # amount = total - promotion
                amount = total - promotion
                description = self.__description(
                    request.POST['name'], request.POST['email'], amount)
                if request.POST.get('stripeToken'):
                    # STRIPE CHARGE
                    charge = StripeService(
                        request.POST['name'],
                        request.POST['email'],
                        request.POST['phone'],
                        int(round(amount)),
                        request.POST['stripeToken'],
                        _('Card Payment')
                    ).call()
                    if charge:
                        BillService(
                            request.user, context['cart'], description, amount, request.POST['address'], charge.id).call()
                        # Send mail
                        subject = 'Hóa đơn mua hàng'
                        html_message = render_to_string('shop/mails/checkout_mail.html', {'cart': context['cart'], 'total': total, 'host': request.get_host})
                        plain_message = strip_tags(html_message)
                        from_email = '<lotus.yoga@gmail.com>'
                        to = request.POST['email']
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                        del request.session['cart']
                        return HttpResponse('success', status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                HttpResponse(e.message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(
                payment_form.errors.as_json(),
                status=status.HTTP_400_BAD_REQUEST)

    def __description(self, name, email, amount):
        listStr = [name, _('with'), _('email'), email, _('paied'), str(amount)]
        result = ' '.join(listStr)
        return result

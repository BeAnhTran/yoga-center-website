from shop.models import Order
from django.db import transaction


class OrderService:
    def __init__(self, user, cart, description, amount, charge_id=None):
        self.user = user
        self.description = description
        self.amount = amount
        self.charge_id = charge_id
        self.cart = cart

    @transaction.atomic
    def call(self):
        order = self.__create_order()
        for item in self.cart:
            order.products.add(item['product'])

    @transaction.atomic
    def __create_order(self):
        order = Order.objects.create(**{
            'user': self.user,
            'description': self.description,
            'amount': self.amount,
            'charge_id': self.charge_id
        })
        return order

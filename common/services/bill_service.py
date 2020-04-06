from shop.models import Bill
from django.db import transaction


class BillService:
    def __init__(self, user, cart, description, amount, shipping_address=None, charge_id=None):
        self.user = user
        self.description = description
        self.amount = amount
        self.charge_id = charge_id
        self.cart = cart
        self.shipping_address = shipping_address

    @transaction.atomic
    def call(self):
        bill = self.__create_bill()
        for item in self.cart:
            bill.products.add(item['product'])

    @transaction.atomic
    def __create_bill(self):
        bill = Bill.objects.create(**{
            'user': self.user,
            'description': self.description,
            'amount': self.amount,
            'charge_id': self.charge_id,
            'shipping_address': self.shipping_address
        })
        return bill

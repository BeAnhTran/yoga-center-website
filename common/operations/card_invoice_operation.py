from card_invoices.models import CardInvoice
from django.db import transaction


class CardInvoiceOperation:
    def __init__(self, card, description, amount, charge_id=None):
        self.card = card
        self.description = description
        self.amount = amount
        self.charge_id = charge_id

    @transaction.atomic
    def call(self):
        CardInvoice.objects.create(**{
            'card': self.card,
            'description': self.description,
            'amount': self.amount,
            'charge_id': self.charge_id
        })

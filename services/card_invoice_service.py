from apps.card_invoices.models import CardInvoice
from django.db import transaction
from apps.card_invoices.models import PREPAID, POSTPAID


class CardInvoiceService:
    def __init__(self, card, payment_type, description, amount, charge_id=None):
        self.card = card
        self.description = description
        self.amount = amount
        self.charge_id = charge_id
        self.payment_type = payment_type

    @transaction.atomic
    def call(self):
        card = CardInvoice.objects.create(**{
            'card': self.card,
            'payment_type': self.payment_type,
            'description': self.description,
            'amount': self.amount,
            'charge_id': self.charge_id
        })
        return card

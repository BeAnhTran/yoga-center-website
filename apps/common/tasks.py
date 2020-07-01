import string
from django.shortcuts import get_object_or_404
from apps.accounts.models import User
from django.utils.crypto import get_random_string
from yoga_center_website.celery import app
from apps.card_invoices.models import CardInvoice


# NOTE: When card has not been payed, delete card after 7 days

@app.task
def removeCardWhenNotPayed(card_invoice_pk):
    card_invoice = get_object_or_404(CardInvoice, pk=card_invoice_pk)
    str = ''
    if card_invoice.is_charged() is False:
        card = card_invoice.card
        yoga_class = card.yogaclass
        str = 'Thẻ tập ' + ' - ' + card.yogaclass.name + ' - Học viên: ' + card.trainee.full_name() + ' đã bị xóa vì chưa thanh toán trong 7 ngày.'
        card.delete()
    else:
        str = 'Thẻ tập đã thanh toán.'
    return str

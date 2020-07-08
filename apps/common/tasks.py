import string
from django.shortcuts import get_object_or_404
from apps.accounts.models import User
from django.utils.crypto import get_random_string
from yoga_center_website.celery import app
from apps.card_invoices.models import CardInvoice, POSTPAID
from notifications.signals import notify
from django.db.models import Q
from celery import shared_task
from django.utils import timezone
from apps.cards.models import Card


@shared_task
def notify_unpaid_card():
    print("===========================================")
    print("Thông báo cho học viên chưa thanh toán thẻ")
    unpaid_cards = Card.objects.filter(
        invoices__charge_id=None, invoices__staff=None).distinct()
    count = 0
    for card in unpaid_cards:
        count += 1
        admin = User.objects.filter(is_superuser=True).first()
        mess = 'Thẻ tập của bạn sẽ hết hạn thanh toán và bị xóa vào ' + str(timezone.localtime(
            card.get_expire_time()).strftime("%d-%m-%Y %H:%M")) + '. Vui lòng thanh toán để không bị gián đoạn.'
        notify.send(sender=admin, recipient=card.trainee.user, verb=mess)
    print("Đã thông báo cho " + str(count) + ' học viên')
    print("===========================================")

# NOTE: When card has not been payed, delete card after 7 days


@app.task
def removeCardWhenNotPayed(card_invoice_pk):
    card_invoice = get_object_or_404(CardInvoice, pk=card_invoice_pk)
    result_str = ''
    if card_invoice.is_charged() is False:
        card = card_invoice.card
        result_str = 'Thẻ tập ' + ' - ' + card.yogaclass.name + ' - Học viên: ' + \
            card.trainee.full_name() + ' đã bị xóa vì chưa thanh toán trong 7 ngày.'
        card.delete()
        admin = User.objects.filter(is_superuser=True).first()
        # send for admins and staffs
        notify.send(sender=admin, recipient=User.objects.filter(Q(is_superuser=True) | Q(is_staff=True)),
                    verb=result_str)
        trainee_str = 'Thẻ tập ' + ' - ' + card.yogaclass.name + \
            ' của bạn đã bị xóa vì chưa thanh toán trong 7 ngày.'
        # send for trainee
        notify.send(sender=admin, recipient=card.trainee.user,
                    verb=trainee_str)
    else:
        result_str = 'Thẻ tập đã thanh toán.'
    return result_str

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required

from datetime import datetime, timedelta
from django.db import transaction
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.db import transaction
from django.utils import timezone
from notifications.signals import notify
from apps.cards.models import Card
from django.utils import timezone


@login_required
@staff_required
@transaction.atomic
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def createNotificationForUnpaidCard(request, pk):
    try:
        card = get_object_or_404(Card, pk=pk)
        mess = 'Thẻ tập của bạn sẽ hết hạn thanh toán và bị xóa vào ' + \
            str(timezone.localtime(card.get_expire_time()).strftime("%d-%m-%Y %H:%M")) + \
            '. Vui lòng thanh toán để không bị gián đoạn.'
        notify.send(sender=request.user,
                    recipient=card.trainee.user, verb=mess)
        return HttpResponse('Tạo thông báo thành công', status=status.HTTP_200_OK)
    except Exception as e:
        return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

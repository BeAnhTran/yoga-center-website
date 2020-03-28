from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from lessons.models import ACTIVE_STATE
from roll_calls.models import RollCall
from roll_calls.serializers import RollCallSerializer
from cards.models import Card
from django.utils.decorators import method_decorator
from core.decorators import trainee_required
from django.contrib.auth.decorators import login_required


@method_decorator([login_required, trainee_required], name='dispatch')
class GetRollCallListApiView(APIView):
    def get(self, request, pk):
        start_date = datetime.fromisoformat(request.GET['startStr'])
        end_date = datetime.fromisoformat(request.GET['endStr'])
        card = get_object_or_404(Card, pk=pk)
        filter_options = {
            'lesson__date__range': [start_date, end_date],
        }
        roll_calls = card.roll_calls.filter(
            **filter_options).order_by('lesson__date')
        serialized = RollCallSerializer(roll_calls, many=True)
        return Response(serialized.data)

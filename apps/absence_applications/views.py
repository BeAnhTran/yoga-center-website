from django.shortcuts import render, redirect, reverse
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.absence_applications.models import AbsenceApplication
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.roll_calls.models import RollCall
from apps.absence_applications.serializers import AbsenceApplicationSerializer


@method_decorator([login_required], name='dispatch')
class AbsenceApplicationApiNewView(APIView):
    def post(self, request):
        roll_call = get_object_or_404(RollCall, pk=request.POST['roll_call'])
        reason = request.POST['reason']
        absence_application = AbsenceApplication.objects.create(
            roll_call=roll_call, reason=reason)
        serializer = AbsenceApplicationSerializer(absence_application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

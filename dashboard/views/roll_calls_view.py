from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required
from roll_calls.models import RollCall
from rest_framework import generics
from roll_calls.serializers import RollCallSerializer


@method_decorator([login_required, staff_required], name='dispatch')
class RollCallDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RollCall.objects.all()
    serializer_class = RollCallSerializer

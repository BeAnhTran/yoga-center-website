from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required
from apps.roll_calls.models import RollCall
from rest_framework import generics
from apps.roll_calls.serializers import RollCallSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


@method_decorator([login_required, staff_required], name='dispatch')
class RollCallDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RollCall.objects.all()
    serializer_class = RollCallSerializer


# Get RollCall for Trainee in Course
@method_decorator([login_required, staff_required], name='dispatch')
class RollCallListViewApi(APIView):
    def get(self, request):
        filter_options = {}
        if request.GET.get('trainee_id'):
            filter_options['card__trainee'] = request.GET.get('trainee_id')
        if request.GET.get('course_id'):
            filter_options['lesson__yogaclass__course'] = request.GET.get(
                'course_id')
        roll_calls = RollCall.objects.filter(**filter_options)
        serialized = RollCallSerializer(roll_calls, many=True)
        return Response(serialized.data)

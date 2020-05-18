from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required
from apps.roll_calls.models import RollCall
from rest_framework import generics
from apps.roll_calls.serializers import RollCallSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.make_up_lessons.models import MakeUpLesson


@method_decorator([login_required, staff_required], name='dispatch')
class RollCallDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RollCall.objects.all()
    serializer_class = RollCallSerializer


# Get RollCall for Trainee in Course
# Roll Call not studied and not have make up lesson
@method_decorator([login_required, staff_required], name='dispatch')
class RollCallListViewApi(APIView):
    def get(self, request):
        filter_options = {}
        if request.GET.get('trainee_id'):
            filter_options['card__trainee'] = request.GET.get('trainee_id')
        if request.GET.get('course_id'):
            filter_options['lesson__yogaclass__course'] = request.GET.get(
                'course_id')
        make_up_lessons_of_trainee = MakeUpLesson.objects.filter(
            lesson__yogaclass__course=request.GET.get('course_id'), roll_call__card__trainee=request.GET.get('trainee_id'))
        filter_options['studied'] = False
        roll_calls = RollCall.objects.filter(**filter_options).exclude(
            id__in=[elem.roll_call.id for elem in make_up_lessons_of_trainee]).distinct()
        serialized = RollCallSerializer(roll_calls, many=True)
        return Response(serialized.data)

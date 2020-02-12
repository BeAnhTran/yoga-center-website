from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from lessons.models import Lesson
from api.serializers import lesson
from datetime import datetime


# Get lessons between startTime and endTime
# Response to schedule
class get_lesson_list_in_range_time(APIView):
    def get(self, request):
        start_date = datetime.fromisoformat(request.GET['startStr'])
        end_date = datetime.fromisoformat(request.GET['endStr'])

        lessons = Lesson.objects.filter(day__range=[start_date, end_date])
        serialized = lesson.lessonSerializer(lessons, many=True)
        return Response(serialized.data)

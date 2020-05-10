from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.lessons.models import Lesson
from apps.lessons.serializers.lesson_serializer import LessonSerializer
from datetime import datetime
from apps.classes.models import YogaClass
from apps.lessons.models import ACTIVE_STATE
# Get lessons between startTime and endTime
# Response to schedule


class GetLessonListInRangeTimeAPIView(APIView):
    def get(self, request):
        start_date = datetime.fromisoformat(request.GET['startStr'])
        end_date = datetime.fromisoformat(request.GET['endStr'])
        if request.GET.get('id_class') is not None:
            id_class = int(request.GET['id_class'])
        else:
            id_class = None
        if request.GET.get('available_only'):
            available_only = request.GET['available_only']
        else:
            available_only = None
        lessons = get_lessons(start_date, end_date, id_class, available_only)
        serialized = LessonSerializer(lessons, many=True)
        return Response(serialized.data)


def get_lessons(start_date, end_date, id_class=None, available_only=None):
    filter_options = {
        'state': ACTIVE_STATE,
        'date__range': [start_date, end_date],
    }
    if available_only is not None:
        filter_options['is_full'] = False

    if id_class is not None:
        yoga_class = YogaClass.objects.get(pk=id_class)
        return yoga_class.lessons.filter(**filter_options).order_by('date')
    else:
        return Lesson.objects.filter(**filter_options).order_by('date')


class LessonDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

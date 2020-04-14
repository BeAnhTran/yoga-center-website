from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required
from apps.roll_calls.models import RollCall
from rest_framework import generics
from apps.roll_calls.serializers import RollCallSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.make_up_lessons.models import MakeUpLesson
from apps.make_up_lessons.serializers import MakeUpLessonSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.lessons.models import Lesson
from apps.cards.models import Card
from apps.core.models import Trainee
from django.views import View
from django.shortcuts import render, redirect, reverse


@method_decorator([login_required, staff_required], name='dispatch')
class MakeUpLessonListApi(APIView):
    def get(self, request, format=None):
        make_up_lessons = MakeUpLesson.objects.all()
        serializer = MakeUpLessonSerializer(make_up_lessons, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        trainee = get_object_or_404(Trainee, pk=request.POST['trainee'])
        roll_call = get_object_or_404(RollCall, pk=request.POST['roll_call'])
        lesson = get_object_or_404(Lesson, pk=request.POST['lesson'])
        check1 = MakeUpLesson.objects.filter(
            lesson=lesson, roll_call__card__trainee=trainee
        )
        if check1:
            return Response('Bạn đã đăng kí học bù', status=status.HTTP_400_BAD_REQUEST)
        is_studied = False
        if int(request.POST.get('is_studied')) == 1:
            is_studied = True
        try:
            make_up_lesson = MakeUpLesson.objects.create(
                roll_call=roll_call, lesson=lesson, is_studied=is_studied)
            serializer = MakeUpLessonSerializer(make_up_lesson)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


@login_required
@staff_required
def delete_make_up_lesson_roll_call(request, lesson_id, pk):
    m = get_object_or_404(MakeUpLesson, pk=pk)
    m.delete()
    return redirect('dashboard:lessons-roll-calls', pk=lesson_id)

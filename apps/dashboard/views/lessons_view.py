from django.http import HttpResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.dashboard.forms.lesssons_form import LessonForm
from apps.lessons.models import Lesson
from apps.lessons.serializers.lesson_serializer import LessonSerializer, LessonUpdateScheduleSerializer
from ..decorators import admin_required, staff_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views import View
from django.shortcuts import render
from django.db import transaction
from datetime import datetime, timedelta
from dateutil import parser
from apps.accounts.models import Trainee, Trainer
from apps.make_up_lessons.models import MakeUpLesson
from django.db.models import Q
from django.shortcuts import get_object_or_404
from apps.lessons.models import TrainerLesson, TAUGHT_STATE, TAUGHT_INSTEAD_STATE
from apps.cards.models import Card
import json


@method_decorator([login_required, staff_required], name='dispatch')
class LessonListView(ListView):
    model = Lesson
    template_name = 'dashboard/lessons/list.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        qs = super(LessonListView, self).get_queryset()
        now = datetime.today()
        if self.request.GET.get('day') and self.request.GET.get('month') and self.request.GET.get('year'):
            d = datetime(
                int(self.request.GET.get('year')),
                int(self.request.GET.get('month')),
                int(self.request.GET.get('day'))
            )
            return qs.filter(date=d)
        return qs.filter(date=now)

    def get_context_data(self, **kwargs):
        context = super(LessonListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'roll_calls'
        if self.request.GET.get('day') and self.request.GET.get('month') and self.request.GET.get('year'):
            d = datetime(
                int(self.request.GET.get('year')),
                int(self.request.GET.get('month')),
                int(self.request.GET.get('day'))
            )
            context['current_date'] = d
        else:
            context['current_date'] = datetime.today()

        bw_date = context['current_date'] - timedelta(days=1)
        fw_date = context['current_date'] + timedelta(days=1)
        context['backward_date'] = bw_date.date
        context['forward_date'] = fw_date.date
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class LessonDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        form = LessonForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            with transaction.atomic():
                lesson = form.save(commit=False)
                lesson.lectures.set(request.POST.getlist('lectures'))
                lesson.save()
                serializer = LessonUpdateScheduleSerializer(lesson)
                return Response(serializer.data)
        return HttpResponse(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        lesson = self.get_object(pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator([login_required, staff_required], name='dispatch')
class ListRollCallApiView(View):
    template_name = 'dashboard/lessons/roll_calls.html'

    def get(self, request, pk):
        lesson = Lesson.objects.get(pk=pk)
        un_studied_roll_calls = lesson.roll_calls.filter(studied=False)
        studied_roll_calls = lesson.roll_calls.filter(studied=True)
        total_count = un_studied_roll_calls.count() + studied_roll_calls.count()
        cards = Card.objects.filter(yogaclass__course=lesson.yogaclass.course).exclude(
            yogaclass=lesson.yogaclass)
        unstudied_make_up_lessons = MakeUpLesson.objects.filter(
            lesson=lesson, is_studied=False)
        studied_make_up_lessons = MakeUpLesson.objects.filter(
            lesson=lesson, is_studied=True)
        available_substitute_trainers = Trainer.objects.filter(
            ~Q(pk=lesson.yogaclass.trainer.pk))

        try:
            taught = TrainerLesson.objects.get(
                lesson=lesson, trainer=lesson.yogaclass.trainer, state=TAUGHT_STATE)
        except TrainerLesson.DoesNotExist:
            taught = None

        try:
            taught_instead = TrainerLesson.objects.get(
                lesson=lesson, trainer=lesson.substitute_trainer, state=TAUGHT_INSTEAD_STATE)
        except TrainerLesson.DoesNotExist:
            taught_instead = None
        print(taught_instead)
        context = {
            'lesson': lesson,
            'un_studied_roll_calls': un_studied_roll_calls,
            'studied_roll_calls': studied_roll_calls,
            'active_nav': 'roll_calls',
            'total_count': total_count,
            'cards': cards,
            'studied_make_up_lessons': studied_make_up_lessons,
            'unstudied_make_up_lessons': unstudied_make_up_lessons,
            'available_substitute_trainers': available_substitute_trainers,
            'taught': taught,
            'taught_instead': taught_instead
        }
        return render(request, self.template_name, context=context)


@method_decorator([login_required, staff_required], name='dispatch')
class SubstituteTrainerApi(APIView):
    def post(self, request, pk, format=None):
        from apps.lessons.utils import check_overlap_in_list_lesson
        sub_trainer = get_object_or_404(
            Trainer, pk=request.POST['sub_trainer'])
        lesson = get_object_or_404(Lesson, pk=pk)
        if lesson.substitute_trainer:
            return Response('Đã có huấn luyện viên dạy bù', status=status.HTTP_400_BAD_REQUEST)
        sub_trainer_lessons_on_day = Lesson.objects.filter(
            date=lesson.date, yogaclass__trainer=sub_trainer)
        check = check_overlap_in_list_lesson(
            lesson.start_time, lesson.end_time, sub_trainer_lessons_on_day)
        if check['value'] is True:
            return Response('HLV bạn chọn đã bận dạy buổi học khác cùng khung giờ', status=status.HTTP_400_BAD_REQUEST)
        try:
            lesson.substitute_trainer = sub_trainer
            lesson.save()
            serializer = LessonSerializer(lesson)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        taught = TrainerLesson.objects.filter(
            lesson=lesson, trainer=lesson.substitute_trainer)
        if taught:
            taught.delete()
        lesson.substitute_trainer = None
        lesson.save()
        return Response('Xóa thành công', status=status.HTTP_200_OK)


@method_decorator([login_required, staff_required], name='dispatch')
class CheckFullLessonApi(APIView):
    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        response_data = {'value': True}
        if lesson.get_all_register_trainee_studing() < lesson.max_people():
            response_data = {'value': False}
        return Response(json.dumps(response_data), status=status.HTTP_200_OK)

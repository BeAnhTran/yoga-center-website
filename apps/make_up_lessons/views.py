from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.make_up_lessons.models import MakeUpLesson
from apps.lessons.models import Lesson
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.roll_calls.models import RollCall
from apps.cards.models import Card
from apps.make_up_lessons.serializers import MakeUpLessonSerializer
from apps.roll_calls.serializers import RollCallSerializer
from apps.refunds.models import Refund, PENDING_STATE, APPROVED_STATE
from apps.absence_applications.models import AbsenceApplication
from django.conf import settings


@method_decorator([login_required], name='dispatch')
class RegisterMakeUpLessonApi(APIView):
    def get(self, request, lesson_pk):
        trainee = request.user.trainee
        lesson = get_object_or_404(Lesson, pk=lesson_pk)
        course = lesson.yogaclass.course
        trainee_course_cards = Card.objects.filter(
            trainee=trainee, yogaclass__course=course)

        # Check that trainee has card for the same course
        if trainee_course_cards.count() < 1:
            return Response(_('You dont have any the same card of course') + ' ' + course.name, status=status.HTTP_400_BAD_REQUEST)
        # Check that lesson is full or not
        if lesson.is_full is True:
            return Response(_('Lesson is full'), status=status.HTTP_400_BAD_REQUEST)
        # Check that trainee has registered this lesson before or not?
        for card in trainee_course_cards:
            for r in card.roll_calls.all():
                if r.lesson == lesson:
                    return Response(_('You have registed at this lesson'), status=status.HTTP_400_BAD_REQUEST)
        # Check that trainee has register this make-up lesson before or not?
        make_up_lessons_of_trainee = MakeUpLesson.objects.filter(
            lesson__yogaclass__course=course, roll_call__card__trainee=trainee)
        for m in make_up_lessons_of_trainee:
            if m.lesson == lesson:
                return Response(_('You have registed a make-up lesson for this lesson'), status=status.HTTP_400_BAD_REQUEST)
        # Check max number of make-up lesson:
        total_number_of_make_up_lessons = 0
        total_max_number_of_make_up_lessons = 0
        for card in trainee_course_cards:
            total_number_of_make_up_lessons += card.get_number_of_make_up_lessons()
            total_max_number_of_make_up_lessons += card.max_number_of_make_up_lessons()
        if total_number_of_make_up_lessons >= total_max_number_of_make_up_lessons:
            message = _('You have registered for up to %(lessons)s/%(max_lesson)s make-up lessons.') % {'lessons': total_number_of_make_up_lessons, 'max_lesson': total_max_number_of_make_up_lessons}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        # Valid RollCall is that has Absence Application
        # Check refund lesson roll call
        # If roll call has refund with state is APPROVE or PENDDING -> ignore)
        absence_applications = AbsenceApplication.objects.filter(
            roll_call__card__trainee=trainee)
        valid_roll_calls = RollCall.objects.filter(card__trainee=trainee, lesson__yogaclass__course=course, studied=False, id__in=[elem.roll_call.id for elem in absence_applications]).exclude(
            refunds__state__in=[PENDING_STATE, APPROVED_STATE]).exclude(id__in=[elem.roll_call.id for elem in make_up_lessons_of_trainee]).distinct()
        serialized = RollCallSerializer(valid_roll_calls, many=True)
        return Response(serialized.data)

    def post(self, request, lesson_pk):
        roll_call = get_object_or_404(RollCall, pk=request.POST['roll_call'])
        if roll_call.is_valid_to_register_make_up_lesson():
            lesson = get_object_or_404(Lesson, pk=lesson_pk)
            make_up_lesson = MakeUpLesson.objects.create(
                roll_call=roll_call, lesson=lesson)
            serializer = MakeUpLessonSerializer(make_up_lesson)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            message = _('Your lesson is expired to make a make-up lesson. You can only register make-up lesson in %(days)s day(s) from the date of lesson. ') % {'days': str(settings.NUMBER_OF_EXPIRE_DAYS_FOR_LESSON)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([login_required], name='dispatch')
class DestroyMakeUpLessonApi(APIView):
    def post(self, request, pk):
        try:
            make_up_lesson = get_object_or_404(MakeUpLesson, pk=pk)
            if request.user.is_superuser is True:
                pass
            else:
                if make_up_lesson.roll_call.card.trainee.user != request.user:
                    return Response(_('You dont have permission'), status=status.HTTP_403_FORBIDDEN)
            make_up_lesson.delete()
            return Response('success', status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

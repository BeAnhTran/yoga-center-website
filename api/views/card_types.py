from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from cards.models import CardType
from api.serializers import card_type

from courses.models import (Course, PRACTICE_COURSE, TRAINING_COURSE)
from django.db.models import Q
from cards.models import (FOR_TRAINING_COURSE)


class get_card_types_for_course(APIView):
    def get(self, request):
        id_course = request.query_params['id_course']
        if id_course is not None:
            course = Course.objects.get(pk=id_course)
            if course.course_type == PRACTICE_COURSE:
                card_types = CardType.objects.filter(
                    ~Q(form_of_using=FOR_TRAINING_COURSE))
            else:
                card_types = CardType.objects.filter(
                    form_of_using=FOR_TRAINING_COURSE)
            serialized = card_type.cardtypeSerializer(card_types, many=True)
            return Response(serialized.data)
        else:
            raise MyException('msg here')

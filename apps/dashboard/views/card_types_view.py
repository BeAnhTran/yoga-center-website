from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required

from apps.card_types.models import (CardType, FOR_TRAINING_COURSE)
from apps.card_types.serializers import CardTypeSerializer
from apps.courses.models import (Course, PRACTICE_COURSE, TRAINING_COURSE)
from django.db.models import Q

@method_decorator([login_required, admin_required], name='dispatch')
class CardTypeListView(ListView):
    model = CardType
    template_name = 'dashboard/card_types/list.html'
    context_object_name = 'card_types'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(CardTypeListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'card_types'
        context['show_nav'] = True
        return context

@method_decorator([login_required, admin_required], name='dispatch')
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
            serialized = CardTypeSerializer(card_types, many=True)
            return Response(serialized.data)
        else:
            raise MyException('msg here')

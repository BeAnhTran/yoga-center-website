from django.http import HttpResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from card_types.models import CardType
from card_types.serializers import CardTypeSerializer


class CardTypeDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return CardType.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        card_type = self.get_object(pk)
        serializer = CardTypeSerializer(card_type)
        return Response(serializer.data)

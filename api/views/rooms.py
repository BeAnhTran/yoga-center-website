from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rooms.models import Room
from api.serializers import room


class get_rooms_list(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serialized = room.roomSerializer(rooms, many=True)
        return Response(serialized.data)
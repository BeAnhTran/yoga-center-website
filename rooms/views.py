from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rooms.models import Room
from rooms.serializers.room_serializer import RoomSerializer


class get_rooms_list(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serialized = RoomSerializer(rooms, many=True)
        return Response(serialized.data)

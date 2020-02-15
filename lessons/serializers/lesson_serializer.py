from rest_framework import serializers
from lessons.models import Lesson

from rooms.serializers.room_serializer import RoomSerializer
from classes.serializers.yoga_class_serializer import YogaClassSerializer
from core.serializers.trainer_serializer import TrainerSerializer


class LessonSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    yogaclass = YogaClassSerializer()
    trainer = TrainerSerializer()

    class Meta:
        model = Lesson
        fields = '__all__'

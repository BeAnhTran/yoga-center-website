from rest_framework import serializers
from make_up_lessons.models import MakeUpLesson

from rooms.serializers.room_serializer import RoomSerializer
from classes.serializers.yoga_class_serializer import YogaClassSerializer
from core.serializers.trainer_serializer import TrainerSerializer

from roll_calls.serializers import RollCallSerializer
from lessons.serializers.lesson_serializer import LessonSerializer
from make_up_lessons.models import MakeUpLesson


class MakeUpLessonSerializer(serializers.ModelSerializer):
    roll_call = RollCallSerializer()
    lesson = LessonSerializer()

    class Meta:
        model = MakeUpLesson
        fields = '__all__'

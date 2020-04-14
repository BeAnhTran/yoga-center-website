from rest_framework import serializers
from apps.make_up_lessons.models import MakeUpLesson

from apps.rooms.serializers.room_serializer import RoomSerializer
from apps.classes.serializers.yoga_class_serializer import YogaClassSerializer
from apps.core.serializers.trainer_serializer import TrainerSerializer

from apps.roll_calls.serializers import RollCallSerializer
from apps.lessons.serializers.lesson_serializer import LessonSerializer
from apps.make_up_lessons.models import MakeUpLesson


class MakeUpLessonSerializer(serializers.ModelSerializer):
    roll_call = RollCallSerializer()
    lesson = LessonSerializer()

    class Meta:
        model = MakeUpLesson
        fields = '__all__'

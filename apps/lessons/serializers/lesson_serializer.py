from rest_framework import serializers
from apps.lessons.models import Lesson

from apps.rooms.serializers.room_serializer import RoomSerializer
from apps.classes.serializers.yoga_class_serializer import YogaClassSerializer
from apps.accounts.serializers.trainer_serializer import TrainerSerializer
from apps.lectures.serializers import LectureSerializer


class LessonSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    yogaclass = YogaClassSerializer()
    substitute_trainer = TrainerSerializer(read_only=True)
    lectures = LectureSerializer(read_only=True, many=True)
    register_trainee_count = serializers.SerializerMethodField()
    max_registrations_number = serializers.SerializerMethodField()
    is_in_the_past = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_register_trainee_count(self, obj):
        return obj.get_all_register_trainee_studing()

    def get_max_registrations_number(self, obj):
        return obj.max_people()

    def get_is_in_the_past(self, obj):
        return obj.is_in_the_past()


class LessonUpdateScheduleSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    yogaclass = YogaClassSerializer()

    class Meta:
        model = Lesson
        exclude = ()

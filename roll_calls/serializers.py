from rest_framework import serializers
from roll_calls.models import RollCall
from lessons.serializers.lesson_serializer import LessonSerializer
from cards.serializers import CardSerializer


class RollCallSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    card = CardSerializer(read_only=True)

    class Meta:
        model = RollCall
        fields = '__all__'

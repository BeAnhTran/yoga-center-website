from rest_framework import serializers
from apps.roll_calls.models import RollCall
from apps.lessons.serializers.lesson_serializer import LessonSerializer
from apps.cards.serializers import CardSerializer


class RollCallSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    card = CardSerializer(read_only=True)

    class Meta:
        model = RollCall
        fields = '__all__'

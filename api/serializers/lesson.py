from rest_framework import serializers
from lessons.models import Lesson


class lessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

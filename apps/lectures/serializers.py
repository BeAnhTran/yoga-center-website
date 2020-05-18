from rest_framework import serializers
from apps.lectures.models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['name', 'description']

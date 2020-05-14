from rest_framework import serializers
from apps.classes.models import YogaClass
from apps.accounts.serializers.trainer_serializer import TrainerSerializer
from apps.courses.serializers import CourseSerializer


class YogaClassSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer()
    course = CourseSerializer()

    class Meta:
        model = YogaClass
        fields = '__all__'

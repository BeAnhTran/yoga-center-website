from rest_framework import serializers
from apps.classes.models import YogaClass
from apps.accounts.serializers.trainer_serializer import TrainerSerializer


class YogaClassSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer()

    class Meta:
        model = YogaClass
        fields = '__all__'

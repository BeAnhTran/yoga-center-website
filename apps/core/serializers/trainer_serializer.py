from rest_framework import serializers

from apps.core.models import Trainer
from apps.core.serializers.user_serializer import UserSerializer


class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainer
        fields = '__all__'

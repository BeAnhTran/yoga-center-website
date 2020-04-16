from rest_framework import serializers

from apps.accounts.models import Trainer
from apps.accounts.serializers.user_serializer import UserSerializer


class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainer
        fields = '__all__'

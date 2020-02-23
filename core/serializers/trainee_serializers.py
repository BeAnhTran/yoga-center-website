from rest_framework import serializers

from core.models import Trainee
from core.serializers.user_serializer import UserSerializer


class TraineeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainee
        fields = '__all__'

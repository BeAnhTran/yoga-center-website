from rest_framework import serializers
from cards.models import Card
from core.serializers.trainee_serializers import TraineeSerializer


class CardSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer()

    class Meta:
        model = Card
        fields = '__all__'

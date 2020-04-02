from rest_framework import serializers
from cards.models import Card, ExtendCardRequest
from core.serializers.trainee_serializers import TraineeSerializer


class CardSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer()

    class Meta:
        model = Card
        fields = '__all__'


class ExtendCardRequestSerializer(serializers.ModelSerializer):
    card = CardSerializer()

    class Meta:
        model = ExtendCardRequest
        fields = '__all__'

from rest_framework import serializers
from apps.cards.models import Card, ExtendCardRequest
from apps.accounts.serializers.trainee_serializer import TraineeSerializer


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

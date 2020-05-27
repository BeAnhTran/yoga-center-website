from rest_framework import serializers
from apps.cards.models import Card
from apps.accounts.serializers.trainee_serializer import TraineeSerializer


class CardSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer()

    class Meta:
        model = Card
        fields = '__all__'

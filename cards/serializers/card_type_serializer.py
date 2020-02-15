from rest_framework import serializers
from cards.models import CardType


class CardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardType
        fields = '__all__'

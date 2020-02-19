from rest_framework import serializers
from card_types.models import CardType


class CardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardType
        fields = '__all__'

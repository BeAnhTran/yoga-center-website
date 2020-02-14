from rest_framework import serializers
from cards.models import CardType


class cardtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardType
        fields = '__all__'

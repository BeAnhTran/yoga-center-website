from rest_framework import serializers
from lessons.models import Lesson

from promotions.models import Promotion
from promotions.serializers.promotion_type_serializer import PromotionTypeSerializer


class PromotionSerializer(serializers.ModelSerializer):
    promotion_types = PromotionTypeSerializer(many=True)

    class Meta:
        model = Promotion
        fields = '__all__'

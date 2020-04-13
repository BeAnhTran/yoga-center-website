from rest_framework import serializers
from lessons.models import Lesson

from promotions.models import PromotionCode
from promotions.serializers.promotion_serializer import PromotionSerializer


class PromotionCodeSerializer(serializers.ModelSerializer):
    promotion = PromotionSerializer()

    class Meta:
        model = PromotionCode
        fields = '__all__'

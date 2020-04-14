from rest_framework import serializers
from apps.lessons.models import Lesson

from apps.promotions.models import PromotionCode
from apps.promotions.serializers.promotion_serializer import PromotionSerializer


class PromotionCodeSerializer(serializers.ModelSerializer):
    promotion = PromotionSerializer()

    class Meta:
        model = PromotionCode
        fields = '__all__'

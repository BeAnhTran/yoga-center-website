from rest_framework import serializers
from apps.lessons.models import Lesson

from apps.promotions.models import Promotion
from apps.promotions.serializers.promotion_type_serializer import PromotionTypeSerializer


class PromotionSerializer(serializers.ModelSerializer):
    promotion_types = PromotionTypeSerializer(many=True)

    class Meta:
        model = Promotion
        fields = '__all__'

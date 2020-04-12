from rest_framework import serializers
from lessons.models import Lesson

from promotions.models import PromotionCode


class PromotionCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionCode
        fields = '__all__'

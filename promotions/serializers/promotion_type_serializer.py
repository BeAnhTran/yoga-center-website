from rest_framework import serializers
from lessons.models import Lesson

from promotions.models import PromotionType


class PromotionTypeSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    full_title = serializers.CharField()

    class Meta:
        model = PromotionType
        fields = '__all__'

    def get_category(self, obj):
        return obj.get_category_display()

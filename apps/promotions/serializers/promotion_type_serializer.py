from rest_framework import serializers
from apps.lessons.models import Lesson

from apps.promotions.models import PromotionType, GIFT_PROMOTION


class PromotionTypeSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    choose_product = serializers.SerializerMethodField()
    full_title = serializers.CharField()

    class Meta:
        model = PromotionType
        fields = '__all__'

    def get_category(self, obj):
        return obj.get_category_display()

    def get_choose_product(self, obj):
        if obj.category == GIFT_PROMOTION:
            return True
        return False

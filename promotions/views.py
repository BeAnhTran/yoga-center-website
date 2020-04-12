from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from promotions.models import PromotionCode
from promotions.serializers.promotion_code_serializers import PromotionCodeSerializer


class CheckCodeApiView(APIView):
    def get(self, request):
        value = request.GET['code']
        promotion_code = get_object_or_404(PromotionCode, value=value)
        serialized = PromotionCodeSerializer(promotion_code)
        return Response(serialized.data)

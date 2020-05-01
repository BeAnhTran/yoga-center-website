from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.promotions.models import PromotionCode, ApplyPromotionCode
from apps.promotions.serializers.promotion_code_serializers import PromotionCodeSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class CheckCodeApiView(APIView):
    def get(self, request):
        value = request.GET['code']
        try:
            promotion_code = get_object_or_404(PromotionCode, value=value)
        except PromotionCode.DoesNotExist:
            return Response({'detail': 'Mã không hợp lệ hoặc đã sử dụng'}, status=status.HTTP_404_NOT_FOUND)
        else:
            apply = ApplyPromotionCode.objects.filter(
                promotion_code=promotion_code).first()
            if apply is not None:
                return Response({'detail': 'Mã không hợp lệ hoặc đã sử dụng'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                serialized = PromotionCodeSerializer(promotion_code)
                return Response(serialized.data)

from rest_framework import serializers
from classes.models import YogaClass


class YogaClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = YogaClass
        fields = '__all__'

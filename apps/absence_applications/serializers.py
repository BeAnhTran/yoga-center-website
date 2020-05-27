from rest_framework import serializers
from apps.absence_applications.models import AbsenceApplication


class AbsenceApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AbsenceApplication
        fields = '__all__'

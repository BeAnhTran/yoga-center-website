from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'phone_number', 'birth_day', 'address', 'image', 'slug')
        # exclude = ('country', 'password')

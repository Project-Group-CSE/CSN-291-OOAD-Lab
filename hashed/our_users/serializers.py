from rest_framework import serializers
from .models import user, credential


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user

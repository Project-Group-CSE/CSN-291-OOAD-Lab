from rest_framework import serializers
from .models import myUser, credential


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = myUser

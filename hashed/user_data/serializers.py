from rest_framework import serializers
from .models import myUser, credential


class UserSerializer(serializers.ModelSerializer):
    credentials = serializers.PrimaryKeyRelatedField(
        many=True, queryset=credential.objects.all()
    )

    class Meta:
        model = myUser
        fields = ["id", "username", "credentials", "hashed_pin"]


"""This means that for each User instance that gets serialized, there will be a credentials field which will 
contain a list of primary keys of credential instances that are related to the User. The many=True argument 
indicates that multiple credential instances can be associated with a single User."""


class CredentialSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = credential
        fields = ["id", "user_name", "title", "website"]

    def get_user_name(self, obj):
        return obj.user.username


"""The SerializerMethodField allows you to customize the representation of a field in a serializer, and in this 
case, it enables you to include the username from the related myUser model in the serialized output of the 
CredentialSerializer."""

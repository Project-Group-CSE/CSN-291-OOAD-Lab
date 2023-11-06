from rest_framework import serializers
from .models import myUser, credential
from encrypt_hash import *

    
class CredentialSerializer(serializers.ModelSerializer):
    user_name = (
        serializers.SerializerMethodField()
    )  
   

    class Meta:
        model = credential
        fields = ["id", "user_name", "title", "website", "hash_pwd","website_username","strength"]
        read_only_fields = ["user_name"]

    def get_user_name(self, obj):
        return obj.user.username
    
 



class CredentialVisibleSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    hash_pwd = serializers.CharField(write_only=True)

    class Meta:
        model = credential
        fields = [
            "id",
            "user_name",
            "title",
            "website",
            "password",
            "hash_pwd",
            "strength",
        ]
        read_only_fields = ["user_name", "password"]

    def get_user_name(self, obj):
        return obj.user.username



class UserListSerializer(serializers.ModelSerializer):
   
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
   
    class Meta:
        model = myUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "hashed_pin",
            "session_token"
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    credentials = serializers.SerializerMethodField()
    """ This field doesn't correspond to a direct attribute of the
     myUser model but allows you to customize the representation of
     credentials for a user"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = myUser
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "credentials",
        ]
        read_only_fields = ["credentials"]

    def get_credentials(self, obj):
        credentials = (
            obj.credential_set.all()
        )  
        return [
            {"id": credential.id, "title": credential.title}
            for credential in credentials
        ] 

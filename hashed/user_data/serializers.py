from rest_framework import serializers
from .models import myUser, credential
from encrypt_hash import *


# Serializer for Credential model
class CredentialSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = credential
        fields = [
            "id",
            "user_name",
            "title",
            "website",
            "hash_pwd",
            "website_username",
            "strength",
        ]
        # Define the fields that are read only
        read_only_fields = ["user_name"]

    # Method to get the username of the user associated with a credential
    def get_user_name(self, obj):
        return obj.user.username

    # Serializer for Credential model with visible password
    # Define fields that get the username and password of the user associated with a credential
    user_name = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    # Define a write only field for hashed password
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
        # Define the fields that are read only
        read_only_fields = ["user_name", "password"]

    # Method to get the username of the user associated with a credential
    def get_user_name(self, obj):
        return obj.user.username


# Serializer for UserList model
class UserListSerializer(serializers.ModelSerializer):
    # Define write only fields for first name, last name and password
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
            "session_token",
        ]


# Serializer for UserDetail model
class UserDetailSerializer(serializers.ModelSerializer):
    credentials = serializers.SerializerMethodField()
    # Define a write only field for password
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
        # Define the fields that are read only
        read_only_fields = ["credentials"]

    # Method to get the credentials of a user
    def get_credentials(self, obj):
        credentials = obj.credential_set.all()
        return [
            {"id": credential.id, "title": credential.title}
            for credential in credentials
        ]

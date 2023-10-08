from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from .models import myUser, credential
from .serializers import UserSerializer, CredentialSerializer


# class CredentialList(generics.ListCreateAPIView):
#     queryset = credential.objects.all()
#     serializer_class = CredentialSerializer


class CredentialDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = credential.objects.all()
    serializer_class = CredentialSerializer


# class UserList(generics.ListAPIView):
#     queryset = myUser.objects.all()
#     serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = myUser.objects.all()
    serializer_class = UserSerializer


# @api_view(["GET"])
# def getData(request):
#     # users = user.objects.all()
#     # serializer = UserSerializer(users, many = true)
#     return Response()  # arg = serializer.data


# @api_view(["POST"])
# def addUser(request):
#     # serializer = UserSerializer(data= request.data)
#     # if serializer.is_valid():
#     # serializer.save()
#     return Response()  # arg = serializer.data

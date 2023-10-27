import uuid
from rest_framework import generics, status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from encrypt_hash import *
from random_good_pass import password_strength
from .models import myUser, credential
from .permissions import isOwner
from .serializers import UserListSerializer, UserDetailSerializer,CredentialSerializer,PinAuthenticationSerializer

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "List of all users": reverse("user_list", request=request, format=format),
            "User Profile": reverse("user_detail", request=request, format=format),
            "List of all credentials of a particular user": reverse(
                "credential_list", request=request, format=format
            ),
        }
    )


@csrf_exempt
def login_view(request):
   
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'message': 'Invalid username or password'})
    return JsonResponse({'message': 'Method not allowed'}, status=405)

    


class CredentialList(generics.ListCreateAPIView):
    serializer_class = CredentialSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def get_queryset(self):
        owner = self.request.user
        queryset = credential.objects.filter(user=owner)
        return queryset
    def list(self, request, *args, **kwargs):
    # Get the PIN from the request or any other source
        pinauth=request.session.get('pin_authenticated',None)
        if pinauth:
            pin =request.session.get('pin',None)
            key=SHA256_hash(pin)
            serializer = self.get_serializer(self.get_queryset(), many=True)
            data=serializer.data.copy()
            for credential in data:
                credential["password"]=decrypt_password(key,credential["hash_pwd"])
                credential["strength"]=password_strength(credential["password"])
                del credential['hash_pwd']
            # error=1/0
            # print(data)
            return Response(serializer.data)
        else:
            redirect=reverse("user_pin_authentication")
            return HttpResponseRedirect(redirect)

    def create(self, request, *args, **kwargs):
        # Handle POST request to create a new credential(encrypt and decrypt)
        data = request.data.copy()
        pin=request.session.get('pin',None)
        
        pinauth=request.session.get('pin_authenticated',None)
        if pinauth:
            password=data["hash_pwd"]
            password_encoded=encrypt_password(SHA256_hash(pin), password, encode=True)
            
            data["hash_pwd"]=password_encoded
            serializer = self.get_serializer(data=data)
            #error=1/0
            if serializer.is_valid():
                serializer.save(user=self.request.user)  # Save the new credential
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            redirect=reverse("user_pin_authentication")
            return HttpResponseRedirect(redirect)


# class CredentialDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = credential.objects.all()
#     serializer_class = CredentialVisibleSerializer
#     permission_classes = (isOwner,)

#     def update(self, request, *args, **kwargs):
#         # Handle PUT request to update an existing credential
#         instance = self.get_object()
#         data = request.data.copy()
#         # manipulate the incoming data here like(password changes)
#         serializer = self.get_serializer(instance, data=data)
#         if serializer.is_valid():
#             serializer.save()  # Update the credential
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListCreateAPIView):
    queryset = myUser.objects.all()
    serializer_class = UserListSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data)
        # manipulate the incoming data here(pin hashing)
        data["hashed_pin"]=str(hash_bcrypt(data["hashed_pin"]))
        password=data["password"]
        data["password"]="-"
        data["id"]=str(uuid.uuid4())
        print(data)
        # data["hashed_pin"]=data["hashed_pin"]+"helo"
        serializer = self.get_serializer(data=data)
        print(serializer)
        print(serializer.is_valid())
        if serializer.is_valid():
            user=serializer.save()
            user.set_password(password)#set_password notifies the django framework
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        #manipulate for passwords
        password=data["password"]
        data["password"]="-"
        serializer = self.get_serializer(instance, data=data,partial=True)
        if serializer.is_valid():
            user=serializer.save()
            user.set_password(password)
            user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class PinAuthenticationView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PinAuthenticationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entered_pin = serializer.validated_data['pin']
        user = request.user

        if check_pin(entered_pin,user.hashed_pin):
            request.session['pin_authenticated'] = True
            request.session['pin']=entered_pin
            redirect=reverse("credential_list")
            return HttpResponseRedirect(redirect)
        else:
            return Response({'detail': 'Invalid PIN. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)

import uuid
from rest_framework import generics, status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from encrypt_hash import *
from user_data.pwd_features import check_password_pwned, get_pass, get_random_pass, password_strength
from .models import myUser, credential
from .permissions import isOwner
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    CredentialSerializer,
    CredentialVisibleSerializer,
)

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
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
   
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = secrets.token_hex(16)
            user.session_token = token
            user.save()
            return JsonResponse({"message": "Success", "token": token})
        else:
            return JsonResponse({"message": "Invalid username or password"})
    return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def get_mem_password(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        
        num = int(data.get("num"))
        caps = data.get("caps")
        cryptify = data.get("cryptify")
        password=get_pass(num,caps,cryptify)
        
        return JsonResponse({"password": password})
@csrf_exempt
def get_random_password(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        
        length = int(data.get("length"))
        nos = data.get("nos")
        symbols = data.get("symbols")
        password=get_random_pass(length,nos,symbols)
        return JsonResponse({"password": password})
    
@csrf_exempt
def get_password_detail(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        
        password=data.get("password")
        pawned=check_password_pwned(password)
        strength=password_strength(password)
        return JsonResponse({"pawned": pawned,"strength":strength})

class CredentialList(generics.ListCreateAPIView):
    serializer_class = CredentialSerializer
    # permission_classes = (permissions.IsAuthenticated,)


    # def get(self, request, *args, **kwargs):
    #     data = json.loads(request.body.decode("utf-8"))
    #     print(data)
    #     token = data.get("session_token")
    #     user = myUser.objects.get(session_token=token)
        
    #     return JsonResponse({"exits":user is not None})
   
    
    
    def get_object(self):
        token = self.request.query_params.get("session_token")
        
        user = myUser.objects.get(session_token=token)
        return user

    def get_queryset(self):
        owner = self.request.user
        queryset = credential.objects.filter(user=owner)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     # Get the PIN from the request or any other source
    #     pinauth = request.session.get("pin_authenticated", None)
    #     if pinauth:
    #         pin = request.session.get("pin", None)
    #         key = SHA256_hash(pin)
    #         serializer = self.get_serializer(self.get_queryset(), many=True)
    #         data = serializer.data.copy()
    #         for credential in data:
    #             credential["password"] = decrypt_password(key, credential["hash_pwd"])
    #             credential["strength"] = password_strength(credential["password"])
    #             del credential["hash_pwd"]
    #         # error=1/0
    #         # print(data)
    #         return Response(serializer.data)
    #     else:
    #         redirect = reverse("user_pin_authentication")
    #         return HttpResponseRedirect(redirect)

    def create(self, request, *args, **kwargs):
        # Handle POST request to create a new credential(encrypt and decrypt)
        entered_pin = request.data.get("pin")
        token = request.data.get("session_token")
        
        instance = myUser.objects.get(session_token=token)
        
        print(entered_pin)
        print(instance.hashed_pin)
        if check_pin(entered_pin, instance.hashed_pin):
            
            data = request.data.copy()
            password = data["hash_pwd"]
            password_encoded = encrypt_password(
                SHA256_hash(entered_pin), password, encode=True
            )
            
            data["hash_pwd"] = password_encoded
            data["id"]=str(uuid.uuid4())
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)  # Save the new credential
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "Invalid PIN. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class CredentialDetail(APIView):
    permission_classes = [isOwner,]
    def get_object(self):
        token = self.request.query_params.get("session_token")
        user = myUser.objects.get(session_token=token)
        return user

    def get_cred(self, pk):
        cred = credential.objects.get(id=pk)
        return cred

    def get(self, request, pk, format=None):
        # This is where you'd return a form for entering the password
        return Response("Please enter your PIN.")

    def post(self, request, pk, format=None):
        entered_pin = request.data.get("pin")
        instance = self.get_object()
        if check_pin(entered_pin, instance.hashed_pin):
            key = SHA256_hash(entered_pin)
            cred = self.get_cred(pk)
            serializer = CredentialVisibleSerializer(cred)
            data = serializer.data.copy()
            data["password"] = decrypt_password(key, data["hash_pwd"])
            data["strength"] = password_strength(data["password"])
            del data["hash_pwd"]
            return Response(data)
        else:
            return Response(
                {"detail": "Invalid PIN. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def put(self, request, pk, format=None):
        instance = self.get_object()
        entered_pin = request.data.get("pin")
        if check_pin(entered_pin, instance.hashed_pin):
            cred = self.get_cred(pk)
            serializer = CredentialVisibleSerializer(cred)
            data = serializer.data.copy()
            password = data["hash_pwd"]
            password_encoded = encrypt_password(
                SHA256_hash(entered_pin), password, encode=True
            )
            data["hash_pwd"] = password_encoded
            serializer = CredentialVisibleSerializer(cred, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "Invalid PIN. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def delete(self, request, pk, format=None):
        cred = self.get_cred(pk)
        cred.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListCreateAPIView):
    queryset = myUser.objects.all()
    serializer_class = UserListSerializer

    def post(self, request, *args, **kwargs):
        queryset = myUser.objects.all()
    serializer_class = UserListSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data)
      
        # manipulate the incoming data here(pin hashing)
        data["hashed_pin"] = (hash_bcrypt(data["hashed_pin"]))
        print(data)
        password = data["password"]
        data["password"] = "-"
        data["id"] = str(uuid.uuid4())
       
        # data["hashed_pin"]=data["hashed_pin"]+"helo"
        serializer = self.get_serializer(data=data)
        print(serializer)
        print(serializer.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # set_password notifies the django framework
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        
        token = self.request.query_params.get("session_token")
        user = myUser.objects.get(session_token=token)
        return JsonResponse({"exists":user is not None})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        
        # manipulate for passwords
        password = data["password"]
        data["password"] = "-"
        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PinAuthenticationView(CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = PinAuthenticationSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         entered_pin = serializer.validated_data["pin"]
#         user = request.user

#         if check_pin(entered_pin, user.hashed_pin):
#             request.session["pin_authenticated"] = True
#             request.session["pin"] = entered_pin
#             redirect = reverse("credential_list")
#             return HttpResponseRedirect(redirect)
#         else:
#             return Response(
#                 {"detail": "Invalid PIN. Please try again."},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )


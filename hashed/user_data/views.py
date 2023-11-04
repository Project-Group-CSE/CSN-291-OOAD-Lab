import uuid
from rest_framework import generics, status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from encrypt_hash import *
from user_data.pwd_features import (
    check_password_pwned,
    get_pass,
    get_random_pass,
    password_strength,
)
from .models import myUser, credential
from .permissions import isOwner
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    CredentialSerializer,
    CredentialVisibleSerializer,
)

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
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
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = secrets.token_hex(16)
            user.session_token = token
            user.save()
            return JsonResponse({"message": "Successfully Logged In", "token": token})
        else:
            return JsonResponse({"message": "Invalid Username or Password"},status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
def get_mem_password(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        num = int(data.get("num"))
        caps = data.get("caps")
        cryptify = data.get("cryptify")
        password = get_pass(num, caps, cryptify)

        return JsonResponse({"password": password})


@csrf_exempt
def get_random_password(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        length = int(data.get("length"))
        nos = data.get("nos")
        symbols = data.get("symbols")
        password = get_random_pass(length, nos, symbols)
        return JsonResponse({"password": password})


@csrf_exempt
def get_password_detail(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        password = data.get("password")
        pawned = check_password_pwned(password)
        strength = password_strength(password)
        return JsonResponse({"pawned": pawned, "strength": strength})


class CredentialList(generics.ListCreateAPIView):
    serializer_class = CredentialSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # def get(self, request, *args, **kwargs):
    #     data = json.loads(request.body.decode("utf-8"))
    #     print(data)
    #     token = data.get("session_token")
    #     user = myUser.objects.get(session_token=token)

    #     return JsonResponse({"exits":user is not None})


    def get_queryset( self, *args, **kwargs):
       
        token = self.request.GET.get("session_token")
        

        owner = myUser.objects.get(session_token=token)
        print(credential.objects.all())
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

      
        if check_pin(entered_pin, instance.hashed_pin):
            data = request.data.copy()
            password = data["hash_pwd"]
            password_encoded = encrypt_password(entered_pin, password, encode=True)
            data.pop("pin", None)
            data.pop("session_token", None)
            data["hash_pwd"] = password_encoded
            data["strength"] = password_strength(password)
            serializer = self.get_serializer(data=data)
            # print(serializer)
            if serializer.is_valid():
                serializer.save(user=instance)  # Save the new credential
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "Invalid PIN. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class CredentialDetail(APIView):
    



    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
       
        entered_pin = request.data.get("pin")
        token = request.data.get("session_token")
        pk=request.data.get("cred_id")
        instance = myUser.objects.get(session_token=token)
        if check_pin(entered_pin, instance.hashed_pin):
            
            key = entered_pin
            cred = credential.objects.get(id=pk)
            data={}
            
            data["password"] = decrypt_password(key, cred.hash_pwd)
            # data["strength"] = password_strength(data["password"])
           
            return Response(data)
        else:
            return Response(
                {},
                status=status.HTTP_401_UNAUTHORIZED,
            )

 
    def put(self, request, format=None):

        entered_pin = request.data.get("pin")
        token = request.data.get("session_token")
        pk=request.data.get("cred_id")
        instance = myUser.objects.get(session_token=token)
        
        
        password=request.data.get("password")
        modified=request.data.get("modified")
        if check_pin(entered_pin, instance.hashed_pin):
            cred = credential.objects.get(id=pk)
            data=request.data.copy()

            if modified:

            
                password_encoded = encrypt_password(entered_pin, password, encode=True)
                data["hash_pwd"] = password_encoded
                data["strength"]=password_strength(password)
            else:
                data["hash_pwd"] = password
            data.pop("modified",None)
            data.pop("password",None)
            data.pop("session_token",None)
            data["user_name"]=cred.user
           
            serializer = CredentialVisibleSerializer(cred,data=data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"strength":data["strength"]},status=status.HTTP_201_CREATED)
           
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def delete(self, request, format=None):
        pk=request.data.get("cred_id")
        cred = credential.objects.all().get(id=pk)
    
        cred.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListCreateAPIView):
    queryset = myUser.objects.all()
    serializer_class = UserListSerializer

    
    
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
      

        # manipulate the incoming data here(pin hashing)
        data["hashed_pin"] = hash_bcrypt(data["hashed_pin"])
    
        password = data["password"]
        data["password"] = "-"
        data["id"] = str(uuid.uuid4())

        # data["hashed_pin"]=data["hashed_pin"]+"helo"
        serializer = self.get_serializer(data=data)
        # print(serializer)
        # print(serializer.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # set_password notifies the django framework
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = self.request.query_params.get("session_token")
      
        try:
            user = myUser.objects.get(session_token=token)
            return JsonResponse({"exists": user is not None,"user": user.username,"firstname":user.first_name,"lastname":user.last_name,"email":user.email})
        except myUser.DoesNotExist:
            user = None
            return JsonResponse({"exists": user is not None})
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        token = request.data.get("session_token")
        instance = myUser.objects.get(session_token=token)
        data = request.data.copy()

        # manipulate for passwords
        # password = data["password"]
        # data["password"] = "-"
        serializer = self.get_serializer(instance, data=data, partial=True)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()    
            # user.set_password(password)
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
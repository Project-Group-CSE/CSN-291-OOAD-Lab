from rest_framework import generics, status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import myUser, credential
from .permissions import isOwner
from .serializers import UserListSerializer, UserDetailSerializer
from .serializers import PinAuthenticationSerializer,CredentialSerializer#, CredentialVisibleSerializer
from encrypt_hash import *
from django.http import HttpResponseRedirect
from random_good_pass import password_strength

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

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # manipulate the incoming data here(pin hashing)
        data["hashed_pin"]=hash_bcrypt(data["hashed_pin"])
        password=data["password"]
        data["password"]="-"
        # data["hashed_pin"]=data["hashed_pin"]+"helo"
        serializer = self.get_serializer(data=data)
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

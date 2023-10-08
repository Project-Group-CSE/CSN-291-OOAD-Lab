from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import myUser, credential
from .permissions import isOwner
from .serializers import UserListSerializer, UserDetailSerializer
from .serializers import CredentialHiddenSerializer, CredentialVisibleSerializer


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
    serializer_class = CredentialHiddenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        owner = self.request.user
        queryset = credential.objects.filter(user=owner)
        return queryset

    def create(self, request, *args, **kwargs):
        # Handle POST request to create a new credential
        data = request.data
        # manipulate the incoming data here
        # data["title"] = data["title"] + "joker"
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)  # Save the new credential
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CredentialDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = credential.objects.all()
    serializer_class = CredentialVisibleSerializer
    permission_classes = (isOwner,)

    def update(self, request, *args, **kwargs):
        # Handle PUT request to update an existing credential
        instance = self.get_object()
        data = request.data
        # manipulate the incoming data here like
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Update the credential
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListCreateAPIView):
    queryset = myUser.objects.all()
    serializer_class = UserListSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        # manipulate the incoming data here
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        # manipulate the incoming data here
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from rest_framework.decorators import api_view  # for fn-based views
from .models import user, credential
from .serializers import UserSerializer


@api_view(["GET"])
def getData(request):
    # users = user.objects.all()
    # serializer = UserSerializer(users, many = true)
    return Response()  # arg = serializer.data


@api_view(["POST"])
def addUser(request):
    # serializer = UserSerializer(data= request.data)
    # if serializer.is_valid():
    # serializer.save()
    return Response()  # arg = serializer.data

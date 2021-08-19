from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.models import User
from users.api.serializers import UserLoginSerializer, UserSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    """
       register api to register a new user to the system
    """
    @action(methods=['post'], detail=False)
    def register(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors, "status": False}, status=status.HTTP_400_BAD_REQUEST)

    """
        login api to log the user to be allowed to use the system
    """
    @action(methods=['post'], detail=False)
    def login(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors, "status": False}, status=status.HTTP_400_BAD_REQUEST)



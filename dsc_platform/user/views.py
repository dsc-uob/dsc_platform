from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from .models import User


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        status_code = status.HTTP_201_CREATED

        return Response(serializer.data, status=status_code)


class UserAccountView(RetrieveUpdateDestroyAPIView):
    """Manage authenticated user."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        if user.is_deleted:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return user

    def delete(self, request, *args, **kwargs):
        user = request.user  # deleting user
        if not user.is_deleted:
            user.is_deleted = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

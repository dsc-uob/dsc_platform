from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer


class UserRegisterView(CreateAPIView):
    """
    Create a new user api.
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserAccountView(RetrieveUpdateDestroyAPIView):
    """Manage authenticated user."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        if user.is_deleted:
            raise NotAuthenticated()
        return user

    def delete(self, request, *args, **kwargs):
        user = request.user
        if not user.is_deleted:
            user.is_deleted = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

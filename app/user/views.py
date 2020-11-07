from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken import views
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.contrib.auth.models import update_last_login

from user import serializers


class CreateUserApi(generics.CreateAPIView):
    """Create and return a new user."""
    serializer_class = serializers.UserSerializer


class LoginView(views.ObtainAuthToken):
    """Create a new token for user."""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        update_last_login(None, user)

        user_data = {
            'token': token.key,
        }
        user_serializer = serializers.UserSerializer(user)
        user_data.update(user_serializer.data)

        return Response(user_data, status=status.HTTP_200_OK)


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage authenticated user."""
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserPhotoView(generics.RetrieveUpdateDestroyAPIView):
    """Manage user photo."""
    serializer_class = serializers.UserPhotoSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        if request.data['photo']:
            return self.update(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.data['photo']:
            return self.partial_update(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)

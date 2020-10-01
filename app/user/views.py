from rest_framework import generics
from rest_framework.authtoken import views
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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
        return Response({
            'token': token.key,
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_authenticated': user.is_authenticated,
            'gender': user.get_gender_display(),
            'stage': user.get_stage_display(),
            'last_login': user.last_login,
            'bio': user.bio
        })

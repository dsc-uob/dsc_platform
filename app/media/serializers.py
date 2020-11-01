from rest_framework.serializers import ModelSerializer

from core import models
from user.serializers import UserSerializer


class ImageSerializer(ModelSerializer):
    """The serializer of image model"""
    user = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = models.Image
        fields = ('id', 'user', 'image', 'created_on')
        read_only_fields = ('id', 'user', 'created_on',)

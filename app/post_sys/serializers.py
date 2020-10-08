from rest_framework import serializers

from core.models import Post
from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""
    user = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'created_on',)
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'created_on': {
                'read_only': True,
            }
        }

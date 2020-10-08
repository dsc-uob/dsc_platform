from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from core import models

from .serializers import PostSerializer
from .permissions import UpdateOwnPermission


class PostViewSet(ModelViewSet):
    """View set from post."""
    serializer_class = PostSerializer
    permission_classes = (UpdateOwnPermission,)
    queryset = models.Post.objects.all()
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        """Return the posts for user."""
        return self.queryset.order_by('-created_on')

    def perform_create(self, serializer):
        """Sets a user for post_sys."""
        serializer.save(user=self.request.user)

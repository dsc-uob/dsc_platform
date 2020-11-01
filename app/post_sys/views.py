from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from core import models
from core.filters import UserOwnFilter
from core.permissions import UpdateOwnPermission

from .serializers import PostSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    """View set from post."""
    serializer_class = PostSerializer
    permission_classes = (UpdateOwnPermission,)
    queryset = models.Post.objects.all()
    authentication_classes = (TokenAuthentication,)
    filter_backends = (UserOwnFilter,)

    def get_queryset(self):
        """Return the posts for user."""
        return self.queryset.order_by('-created_on')

    def perform_create(self, serializer):
        """Sets a user for post_sys."""
        serializer.save(user=self.request.user)


class CommentSetView(ModelViewSet):
    """API View comment."""
    serializer_class = CommentSerializer
    permission_classes = (UpdateOwnPermission,)
    queryset = models.Comment.objects.all()
    authentication_classes = (TokenAuthentication,)
    filter_backends = (UserOwnFilter,)

    def get_queryset(self):
        """Get the current comments."""
        post_id = self.request.query_params.get('post')
        return self.queryset.filter(post_id=post_id)

    def perform_create(self, serializer):
        """Sets a user comment."""
        serializer.save(user=self.request.user,
                        post_id=self.request.data['post'])

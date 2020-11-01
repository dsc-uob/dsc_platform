from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from core import models, permissions
from core.filters import UserOwnFilter

from . import serializers


class ImageViewSet(ModelViewSet):
    """View set of image."""
    serializer_class = serializers.ImageSerializer
    permission_classes = (permissions.UpdateOwnPermission,)
    queryset = models.Image.objects.all()
    authentication_classes = (TokenAuthentication,)
    filter_backends = (UserOwnFilter,)

    def get_queryset(self):
        """Return all images."""
        return self.queryset.order_by('-created_on')

    def perform_create(self, serializer):
        """Sets a user for image."""
        serializer.save(user=self.request.user)

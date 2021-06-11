from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotAcceptable
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import permissions
from . import serializers
from . import models
from . import filters


class ArticleViewset(ModelViewSet):
    """
    View of article model.
    """
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.order_by('-created_date')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.PostPermission,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleCommentViewset(ModelViewSet):
    """
    View of article comment model.
    """
    serializer_class = serializers.ArticleCommentSerializer
    queryset = models.ArticleComment.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.PostPermission,)
    filter_backends = [filters.ArticleCommentFilter, ]

    def perform_create(self, serializer):
        article_id = self.request.query_params.get('article')
        if article_id is None:
            raise NotAcceptable('Could not created, no article id in query params.')
        serializer.save(user=self.request.user,
                        article_id=self.request.query_params.get('article'), )


class EnquiryViewset(ModelViewSet):
    """
    Viewset of enquiry model.
    """
    serializer_class = serializers.EnquirySerializer
    queryset = models.Enquiry.objects.order_by('-created_date')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.PostPermission,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EnquiryCommentViewset(ModelViewSet):
    """
    View of enquiry comment model.
    """
    serializer_class = serializers.EnquiryCommentSerializer
    queryset = models.EnquiryComment.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.PostPermission,)
    filter_backends = [filters.EnquiryCommentFilter, ]

    def perform_create(self, serializer):
        enquiry_id = self.request.query_params.get('enquiry')
        if enquiry_id is None:
            raise NotAcceptable('Could not created, no enquiry id in query params.')
        serializer.save(user=self.request.user,
                        enquiry_id=self.request.query_params.get('enquiry'), )

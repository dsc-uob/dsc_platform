from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied

from django.core.exceptions import ObjectDoesNotExist

from core import permissions
from core import models
from core import filters
from . import serializers


class CreateChatSessionView(generics.CreateAPIView):
    """Create a new chat session view."""
    queryset = models.ChatSession.objects.all()
    serializer_class = serializers.ChatSessionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Sets a user for chat session."""
        obj = serializer.save(owner=self.request.user)
        models.ChatMember.objects.get_or_create(
            chat_session=obj,
            user=self.request.user,
        )


class ListChatSessionView(generics.ListAPIView):
    """List my chat session view."""
    serializer_class = serializers.ChatMemberSerializer
    queryset = models.ChatMember.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnPermission,)

    def get_queryset(self):
        """Return the chat sessions for user."""
        return self.queryset.filter(
            user_id=self.request.user.id
        ).order_by('-updated_date')


class ManageChatSessionView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve or update or delete a model."""

    serializer_class = serializers.ChatSessionSerializer
    queryset = models.ChatSession.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.ManageSessionPermission,)


class ChatMessageView(ModelViewSet):
    """Create/Get Chat messages."""

    serializer_class = serializers.ChatMessageSerializer
    queryset = models.ChatMessage.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.SessionMemberPermission,)
    filter_backends = (filters.UserOwnFilter,)

    def get_queryset(self):
        """Return the chat sessions for user."""
        chat_session_id = self.request.query_params.get('chat_session')
        return self.queryset.filter(
            chat_session_id=chat_session_id,
        ).order_by('-updated_date')

    def perform_create(self, serializer):
        """Sets a user for post_sys."""
        chat_session_id = serializer.validated_data['chat_session']
        chat_session = models.ChatSession.objects.get(
            id=chat_session_id
        )
        try:
            chat_session.members.get(
                user=self.request.user,
            )
            serializer.save(user=self.request.user)
        except ObjectDoesNotExist:
            raise PermissionDenied(
                detail='Only chat members can send a new message!',
            )


class ChatRoleView(ModelViewSet):
    """The view set of chat role model."""

    serializer_class = serializers.ChatRoleSerializer
    queryset = models.ChatRole.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.SessionMemberPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('title',)

    def get_queryset(self):
        """Return the chat sessions for user."""
        chat_session_id = self.request.query_params.get('chat_session')
        return self.queryset.filter(
            chat_session_id=chat_session_id,
        ).order_by('-updated_date')

    def perform_create(self, serializer):
        chat_session_id = serializer.validated_data['chat_session']
        chat_session = models.ChatSession.objects.get(
            id=chat_session_id
        )
        if chat_session.owner.id == self.request.user.id:
            serializer.save()
        else:
            raise PermissionDenied(
                detail='Only owner can add a new role!'
            )

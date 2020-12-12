from rest_framework.serializers import ModelSerializer, \
    ListField

from core import models
from user import serializers


# ChatRole section
class ChatRoleSerializer(ModelSerializer):
    """The class serializer of chat role."""

    class Meta:
        model = models.ChatRole
        fields = '__all__'
        read_only_fields = ('id',)


# ChatSession section
def add_members(chat_session, members):
    """Add member to chat session."""
    for member in members:
        user = models.User.objects.get(
            id=member,
        )
        models.ChatMember.objects.get_or_create(
            user=user,
            chat_session=chat_session,
        )


def remove_members(chat_session, members):
    """Remove member from chat session."""
    for member in members:
        removed_member = models.ChatMember.objects.get(
            id=member,
            chat_session=chat_session,
        )
        removed_member.delete()


class _ChatMemberSerializerForChatSessionSerializer(ModelSerializer):
    """This serializer only for ChatSessionSerializer"""
    user = serializers.UserSerializer(
        read_only=True
    )

    class Meta:
        model = models.ChatMember
        exclude = ['chat_session', ]
        read_only_fields = ('id', 'chat_session')


class _LimitChatRoleSerializer(ModelSerializer):
    """The class serializer of chat role."""

    class Meta:
        model = models.ChatRole
        exclude = ['chat_session', ]
        read_only_fields = ('id',)


class ChatSessionSerializer(ModelSerializer):
    """The serializer class of chat session."""
    owner = serializers.UserSerializer(
        read_only=True
    )

    members = _ChatMemberSerializerForChatSessionSerializer(
        read_only=True,
        many=True,
    )
    roles = _LimitChatRoleSerializer(
        read_only=True,
        many=True,
    )

    # custom serializer field to control session members.
    # @add_members for adding new members to session.
    add_members = ListField(
        write_only=True,
        required=False,
    )
    # @remove_members for removing members from session.
    remove_members = ListField(
        write_only=True,
        required=False,
    )

    class Meta:
        model = models.ChatSession
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):
        members = validated_data.pop('add_members', None)
        chat_session = models.ChatSession.objects.create(**validated_data)
        if members:
            add_members(
                chat_session=chat_session,
                members=members
            )
        return chat_session

    def update(self, instance, validated_data):
        # Add new members to chat session.
        members = validated_data.pop('add_members', None)
        if members:
            add_members(
                chat_session=instance,
                members=members
            )

        # Remove members from chat session.
        members = validated_data.pop('remove_members', None)
        if validated_data.get('remove_members'):
            remove_members(
                chat_session=instance,
                members=members
            )

        return super().update(instance, validated_data)


# ChatMember section
class _ChatSessionSerializerForMember(ModelSerializer):
    """This serializer only for ChatMemberSerializer"""

    class Meta:
        model = models.ChatSession
        exclude = ['owner', ]
        read_only_fields = ('id',)


class ChatMemberSerializer(ModelSerializer):
    """The serializer class of chat member."""
    chat_session = _ChatSessionSerializerForMember(
        read_only=True,
    )
    role = _LimitChatRoleSerializer(
        read_only=True,
    )

    class Meta:
        model = models.ChatMember
        exclude = ['user', ]
        read_only_fields = ('id',)


# ChatMessage section
class ChatMessageSerializer(ModelSerializer):
    """The serializer class of chat message."""
    user = serializers.UserSerializer(
        read_only=True
    )

    class Meta:
        model = models.ChatMessage
        fields = '__all__'
        read_only_fields = ('id', 'user')

    def update(self, instance, validated_data):
        validated_data.pop('parent', None)
        validated_data.pop('chat_session', None)
        chat_message = super().update(instance, validated_data)

        return chat_message

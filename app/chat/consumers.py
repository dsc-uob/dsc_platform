from core import models
from core import consumers
from . import serializers


class ManageChatSessionConsumer(consumers.GenericWebsocketConsumer):
    """List my chat session consumer."""

    queryset = models.ChatSession.objects.all()
    serializer_class = serializers.ChatSessionSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_session_id = None

    def register_groups(self, kwargs):
        self.chat_session_id = kwargs['chat_session']
        return [
            self.chat_session_id,
        ]

    def receive_json(self, content, **kwargs):
        serializer = self.get_serializer(id=self.chat_session_id)
        data = serializer.data

        self.group_send_json(
            event_type='chat.session',
            group=self.chat_session_id,
            content=data,
        )

    def chat_session(self, event):
        self.send_json(event)


class ChatMessageConsumer(consumers.GenericWebsocketConsumer):
    """For chat messages."""

    queryset = models.ChatMessage.objects.all()
    serializer_class = serializers.ChatMessageSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_session_id = None

    def register_groups(self, kwargs):
        self.chat_session_id = kwargs['chat_session']
        return [
            self.chat_session_id,
        ]

    def receive_json(self, content, **kwargs):
        message = content['message']
        message['chat_session'] = self.chat_session_id
        if message['body']:
            serializer = self.serializer_class(data=message)
            if serializer.is_valid():
                serializer.save(user=self.user)
                self.group_send_json(
                    event_type='chat.message',
                    group=self.chat_session_id,
                    content=serializer.data,
                )

    def chat_message(self, event):
        self.send_json(event)

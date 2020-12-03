from django.urls import re_path

from .consumers import ChatMessageConsumer, ManageChatSessionConsumer

websocket_urlpatterns = [
    re_path(r"^chat/session/(?P<chat_session>[\w.@+-]+)/$",
            ManageChatSessionConsumer.as_asgi()),
    re_path(r"^chat/messages/(?P<chat_session>[\w.@+-]+)/$",
            ChatMessageConsumer.as_asgi()),
]

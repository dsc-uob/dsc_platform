from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from chat import consumers

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                url(r"^chat/session/(?P<chat_session>[\w.@+-]+)/$",
                    consumers.ManageChatSessionConsumer.as_asgi()),
                url(r"^chat/messages/(?P<chat_session>[\w.@+-]+)/$",
                    consumers.ChatMessageConsumer.as_asgi()),
            ])
        )
    ),
})

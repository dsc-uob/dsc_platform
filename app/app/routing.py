from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

from chat import routing as cr
from test import routing as tr

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                cr.websocket_urlpatterns +
                tr.websocket_urlpatterns,
            )
        )
    ),
})

from django.urls import re_path

from .consumers import TestConsumer

websocket_urlpatterns = [
    re_path(r'', TestConsumer.as_asgi()),
]

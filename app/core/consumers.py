from asgiref.sync import async_to_sync

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token

from channels.generic.websocket import JsonWebsocketConsumer
from channels.exceptions import InvalidChannelLayerError, \
    DenyConnection, AcceptConnection


class NoTokenProvided(Exception):
    pass


class UnauthenticatedUser(Exception):
    pass


def get_user_by_token(token):
    """
    Get the user within provided token, this is function
    specified for consumer sub-classes.
    """
    # Check if token available
    if not token:
        raise NoTokenProvided()

    # Try to get user with provided token key,
    # it will throw an exception if no user found!
    token = token.split(' ')[-1]
    user = Token.objects.get(key=token).user
    return user


class GenericWebsocketConsumer(JsonWebsocketConsumer):
    """
    Base class for all other generic consumers.
    """

    queryset = None
    serializer_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {}
        self.user = None

    # Connection section
    def websocket_connect(self, message):
        """
        Called when a WebSocket connection is opened.
        """
        self.prepare_headers()
        try:
            kwargs = self.scope['url_route']['kwargs']
            groups = self.register_groups(kwargs)
            for group in groups:
                async_to_sync(self.channel_layer.
                              group_add)(group, self.channel_name)
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        try:
            self.connect()
        except AcceptConnection:
            self.accept()
        except DenyConnection:
            self.close()
        except UnauthenticatedUser:
            self.close(code=401)

    def connect(self):
        self.check_authentication()
        super().connect()

    def check_authentication(self):
        """
        Check the connection authentication.
        """
        if 'token' not in self.headers:
            raise UnauthenticatedUser()
        try:
            user = get_user_by_token(self.headers['token'])
            self.user = user
        except ObjectDoesNotExist:
            raise UnauthenticatedUser()

    def prepare_headers(self):
        """
        Provider the headers.
        """
        headers = dict(self.scope['headers'])
        for header in headers:
            self.headers[header.decode("utf-8")] = \
                headers[header].decode("utf-8")

    # Send & Group section
    def register_groups(self, kwargs):
        """
        Return a list of string include the groups
        that you need to register in this channel.
        """
        return []

    def group_send_json(self, group: str, content,
                        event_type: str, close=False):
        """
        Send a data for specific group, with and data type.

        params:
        @group: for selected group that will be receive the message
        @content: the data will send
        @event_type: the name of event will call when send message,
                     you must provide a function within event name.
        """
        if group is not None and content is not None:
            event = {
                "type": event_type,
                "text": self.encode_json(content)
            }
            async_to_sync(self.channel_layer.group_send)(
                group,
                message=event
            )

        else:
            raise ValueError("You must pass one of bytes_data or text_data")
        if close:
            self.close(close)

    # Query & Object section
    def get_object(self, **kwargs):
        """
        Get one object from [kwargs] data.
        """
        queryset = self.get_queryset()
        obj = queryset.get(**kwargs)
        return obj

    def get_serializer(self, **kwargs):
        """
        Get one serialized object from [kwargs] data.
        """
        obj = self.get_object(**kwargs)
        serializer = self.serializer_class(obj)
        return serializer

    def get_queryset(self):
        """
        Gel queryset
        """

        if not self.queryset:
            raise ValueError(
                "You mush provide a queryset"
            )

        return self.queryset.all()

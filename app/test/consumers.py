from channels.generic.websocket import JsonWebsocketConsumer


class TestConsumer(JsonWebsocketConsumer):

    def websocket_connect(self, message):
        super(TestConsumer, self).websocket_connect(message)
        self.send_json('Connected Successfully!')

    def receive_json(self, content, **kwargs):
        message = content['message']
        self.send_json(message)

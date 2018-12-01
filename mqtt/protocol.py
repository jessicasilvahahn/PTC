import asyncio
from mqtt.messages.publish import Publish
from mqtt.messages.connect import Connect
from mqtt.messages.subscribe import Subscribe


class publish_protocol(asyncio.Protocol):
    def __init__(self, topic, value, loop):
        publish_message = Publish()
        publish_message.mount_message(topic, value)
        self.message = publish_message.get_complete_packet()
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message)
        print('Publish sent')

    def data_received(self, data):
        print('Received unexpected response when publishing')

    # We should treat the possible exception exc
    def connection_lost(self, exc):
        print('Publish transaction ended, closing connection')
        self.loop.stop()


class connection_protocol(asyncio.Protocol):
    # See if is necessary to send a client_id,
    # because there is a hardcoded client id in Connect code...
    def __init__(self, loop, set_connection_handler):
        connect_message = Connect()
        connect_message.mount_message()
        self.message = connect_message.get_complete_packet()
        self.loop = loop
        self.set_connection = set_connection_handler

    def connection_made(self, transport):
        transport.write(self.message)
        print('Connection packet sent')

    def data_received(self, data):
        connect_parser = Connect()
        if (connect_parser.parse_connack(data)):
            self.set_connection(True)
            print('Accepted connection')
            return
        self.set_connection(False)
        print('Refused connection')

    # We should treat the possible exception exc
    def connection_lost(self, exc):
        print('Connect transaction is finished')


class subscribe_protocol(asyncio.Protocol):
    def __init__(self, topic_name, loop):
        subscribe_message = Subscribe()
        subscribe_message.mount_message(topic_name)
        self.message = subscribe_message.get_complete_packet()
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message)
        print('Subscribe packet sent')

    def data_received(self, data):
        subscribe_parser = Subscribe()
        if (subscribe_parser.parse_suback(data)):
            print('Client subscribed')
            return
        print('Subescribe rejeitado pelo broker')

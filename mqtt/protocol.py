import asyncio
from messages.publish import Publish
from messages.connect import Connect

# Mocking a state, we should see how it will work,
# maybe use a global variable, or put this control
# in the behaivioral class


def set_connected(connection_status):
    is_connected = connection_status


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
    def __init__(self, loop):
        connect_message = Connect()
        connect_message.mount_message()
        self.message = connect_message.get_complete_packet()
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message)
        print('Connection packet sent')

    def data_received(self, data):
        connect_parser = Connect()
        if (connect_parser.parse_connack(data)):
            set_connected(True)
            print('Accepted connection')
            return
        print('Refused connection')

    # We should treat the possible exception exc
    def connection_lost(self, exc):
        print('Connect transaction is done')


class subscribe_protocol():
    pass

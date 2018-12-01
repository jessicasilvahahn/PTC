import asyncio

from mqtt.protocol import connection_protocol
from mqtt.protocol import publish_protocol
from mqtt.protocol import subscribe_protocol
from mqtt.listener import Listener


def publish(address, topic, value):
    if (not __connect(address)):
        print('Sorry, unable to connect')
        return False
    else:
        loop = asyncio.get_event_loop()
        publish = loop.create_connection(
            lambda: publish_protocol(topic, value, loop),
            address, 1883)
        loop.run_until_complete(publish)
        return True


def subscribe(address, topic, callback):
    if(not __connect(address)):
        print('Sorry, unable to connect')
        return None
    else:
        loop = asyncio.get_event_loop()
        subscribe = loop.create_connection(
            lambda: subscribe_protocol(topic, loop),
            address, 1883)
        loop.run_until_complete(subscribe)
        listener = __listen_on(address, callback)
        return listener


def __connect(address):
    is_connected = False

    def connection_handler(status):
        nonlocal is_connected
        is_connected = status

    loop = asyncio.get_event_loop()
    connection = loop.create_connection(
        lambda: connection_protocol(loop, connection_handler),
        address, 1883)
    loop.run_until_complete(connection)

    return is_connected


def __listen_on(address, callback):
    loop = asyncio.get_event_loop()
    listener = loop.create_server(lambda: Listener(callback), address, 1883)
    server = loop.run_until_complete(listener)
    loop.run_forever()
    return server

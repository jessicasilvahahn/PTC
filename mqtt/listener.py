import asyncio


class Listener(asyncio.Protocol):
    def __init__(self, callback):
        self.callback = callback

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.transport.close()
        self.callback(data)

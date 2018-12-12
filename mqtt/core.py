import socket
from mqtt.protocol import connection_protocol
from mqtt.protocol import publish_protocol
from mqtt.protocol import subscribe_protocol
from mqtt.protocol import unsubscribe_protocol

class core():

    def __init__(self,address):
        self.address = address
        self.port = 1883
        self.buffer_size = 2048
        self.channel = None
        self.loop = True

    def publish(self,topic, value):
        if (not self.__connect()):
            print('Sorry, unable to connect')
            return False
        else:
            publish = publish_protocol(topic,value,self.channel)
            return publish.connection_made()


    def subscribe(self, topic):
        if(not self.__connect()):
            print('Sorry, unable to connect')
            return False
        else:
            subscribe = subscribe_protocol(topic,self.channel)
            subscribe.connection_made()
            self.loop = True
            while(self.loop):
                if(subscribe.suback and subscribe.publish):
                    subscribe.suback = False
                    subscribe.publish = False
                    self.loop = False
                else:
                    data = self.channel.recv(self.buffer_size)
                    if(data!=b''):
                        self.loop = subscribe.data_received(data)
            return (subscribe.data_received(data),data)



    def unsubscribe(self,topic):
        if (not self.__connect()):
            print('Sorry, unable to connect')
            return False
        else:
            unsubscribe = unsubscribe_protocol(topic,self.channel)
            unsubscribe.connection_made()
            self.loop = True
            while(self.loop):
                data = self.channel.recv(self.buffer_size)
                if (data!=b''):
                    self.loop = False
            return unsubscribe.data_received(data)



    def __connect(self):
        try:
            self.channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.channel.connect((self.address, self.port))
            connection = connection_protocol(self.channel)
            connection.connection_made()
            self.loop = True
            while(self.loop):
                data = self.channel.recv(self.buffer_size)
                if(data!=b'' and data[0]==32):
                    self.loop = False
            connection.data_received(data)
            return connection.set_connection
        except socket.error as e:
            raise e





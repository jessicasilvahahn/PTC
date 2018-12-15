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
        self.__channel = None
        self.__connected = None
        self.loop = True
        self.__sub = None
        self.__unsub = None

    def publish(self,topic, value,retain):
        if (not self.__connect()):
            print('Sorry, unable to connect')
            return False
        else:
            publish = publish_protocol(topic,value,self.__channel,retain)
            return publish.connection_made()


    def subscribe(self, topic):
        if(self.__channel!=None and self.__connected):
            data = self.__channel.recv(self.buffer_size)
            if (data != b''):
                r = self.__sub.data_received(data)
            return (r,data)
        else:
            self.__connected = self.__connect()
            if(not self.__connected):
                print('Sorry, unable to connect')
                return False
            else:
                self.loop = True
                self.__sub = subscribe_protocol(topic, self.__channel)
                self.__sub.connection_made()
                (r,data) = self.__send_subscribe(self.__sub)
                return (r,data)

    def __send_subscribe(self,subscribe):
        while (self.loop):
            if (subscribe.suback):
                subscribe.suback = False
                self.loop = False
            else:
                data = self.__channel.recv(self.buffer_size)
                if (data != b''):
                    self.loop = subscribe.data_received(data)
        return (subscribe.data_received(data), data)

    def get_pulish_received(self):
        if(self.__sub!=None):
            return self.__sub.publish
        else:
            return False

    def unsubscribe(self,topic):
        if (self.__channel != None and self.__connected and (self.__unsub!=None)):
            data = self.__channel.recv(self.buffer_size)
            if (data != b''):
                print(self.__unsub)
                r = self.__unsub.data_received(data)
                return (r)
        else:
            self.__connected = self.__connect()
            if (not self.__connected):
                print('Sorry, unable to connect')
                return False
            return self.__send_unsubscribe(topic)

    def __send_unsubscribe(self,topic):
        self.__unsub = unsubscribe_protocol(topic, self.__channel)
        self.__unsub.connection_made()
        self.loop = True
        while (self.loop):
            if (self.__unsub.unsuback):
                self.__unsub.suback = False
                self.loop = False
            else:
                data = self.__channel.recv(self.buffer_size)
                if (data != b''):
                    self.loop = False
        return self.__unsub.data_received(data)

    def __connect(self):
        try:
            self.__channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__channel.connect((self.address, self.port))
            connection = connection_protocol(self.__channel)
            connection.connection_made()
            self.loop = True
            while(self.loop):
                data = self.__channel.recv(self.buffer_size)
                if(data!=b'' and data[0]==32):
                    self.loop = False
            connection.data_received(data)
            return connection.set_connection
        except socket.error as e:
            raise e

    def close(self):
        self.__channel.close()





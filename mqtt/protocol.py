import socket
from mqtt.messages.publish import Publish
from mqtt.messages.connect import Connect
from mqtt.messages.subscribe import Subscribe
from mqtt.messages.unsubscribe import Unsubscribe


class publish_protocol():
    def __init__(self, topic, value, channel):
        self.channel = channel
        if(len(topic) > 255):
            print("size isn't allowed\n")
            print("size need to be less than 256\n")
            self.connection_lost()
        publish_message = Publish()
        publish_message.mount_message(topic, value)
        self.message = publish_message.get_complete_packet()


    def connection_made(self):
        if(not self.message):
            self.connection_lost()
        else:
            self.channel.send(self.message)
            print('Publish sent')
            return True


    def connection_lost(self):
        self.channel.close()
        raise ValueError("Publish transaction ended, closing connection")


class connection_protocol():
    def __init__(self, channel):
        connect_message = Connect()
        connect_message.mount_message()
        self.message = connect_message.get_complete_packet()
        self.set_connection = False
        self.channel = channel

    def connection_made(self):
        if(not self.message):
            self.connection_lost()
        else:
            self.channel.send(self.message)
            print('Connection packet sent')

    def data_received(self, data):
        connect_parser = Connect()
        if (connect_parser.parse_connack(data)):
            self.set_connection = True
            print('Accepted connection')
            return
        self.set_connection = False
        print('Refused connection')
        self.connection_lost()

    def connection_lost(self):
        self.channel.close()
        raise ValueError('Connect transaction is finished')


class subscribe_protocol():
    def __init__(self, topic_name, channel):
        self.channel = channel
        if (len(topic_name) > 255):
            print("size isn't allowed\n")
            print("size need to be less than 256\n")
            self.connection_lost()
        subscribe_message = Subscribe()
        subscribe_message.mount_message(topic_name)
        self.message = subscribe_message.get_complete_packet()
        self.publish = False
        self.suback = False


    def connection_made(self):
        if(not self.message):
            self.connection_lost()
        else:
            self.channel.send(self.message)
            print('Subscribe packet sent')
            return

    def data_received(self, data):
        print("Data Received:",data)
        subscribe_parser = Subscribe()
        if (subscribe_parser.parse_suback(data)):
            print('Client subscribed')
            self.suback = True
            return True
        else:
            if (subscribe_parser.parse_publish(data)):
                print("Client received publish")
                self.publish = True
                return True
            else:
                if(data[0] == 144):
                    print('Subscribe rejected by broker')
                    self.connection_lost()
                    return False
                else:
                    print("Packet isn't subscribe or publish")
                    return True

    def connection_lost(self):
        self.channel.close()
        raise ValueError('Subscribe transaction is finished')

class unsubscribe_protocol():
    def __init__(self, topic_name, channel):
        self.channel = channel
        if (len(topic_name) > 255):
            print("size isn't allowed\n")
            print("size need to be less than 256\n")
            self.connection_lost()
        unsubscribe_message = Unsubscribe()
        unsubscribe_message.mount_message(topic_name)
        self.message = unsubscribe_message.get_complete_packet()


    def connection_made(self):
        if(not self.message):
            self.connection_lost()
        else:
            self.channel.send(self.message)
            print('Unsubscribe packet sent')
            return


    def data_received(self, data):
        unsubscribe_parser = Unsubscribe()
        if (unsubscribe_parser.parse_unsuback(data)):
            print('Client unsubscribed')
            return True
        print('Unsubscribe reject by broker')
        self.connection_lost()
        return False

    def connection_lost(self):
        self.channel.close()
        raise ValueError('Unsubscribe transaction is finished')



from mqtt.messages.message import Message


class Subscribe(Message):

    def __init__(self):
        super().__init__()

    def mount_message(self, topic_name):
        if (isinstance(topic_name, str)):
            self.packet['fixed_header'] = b'\x82'
            packet_identifier = b'\x00' + b'\x01'
            qos = b'\x00'
            topic_name_size = b'\x00' + bytes(bytearray([len(topic_name)]))

            self.packet['variable_header'] = packet_identifier

            self.packet['payload'] = topic_name_size + \
                topic_name.encode('utf-8') + qos

            remaining_size = self.get_remaining_size(
                len(self.packet['variable_header'] + self.packet['payload']))
            if (not remaining_size):
                self.packet = None
            else:
                self.packet['fixed_header'] = self.packet['fixed_header'] + \
                    remaining_size

    def parse_suback(self, suback):
        if(suback[0] == 144):
            if(suback[-1] == 0):
                return True
            else:
                return False
        else:
            print("Isn't suback\n")
            return False

    def parse_publish(self,publish):
        if(publish[0] == 48 or publish[0] == 49 ):
            return True
        else:
            return False
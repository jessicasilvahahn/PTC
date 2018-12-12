from mqtt.messages.message import Message


class Unsubscribe(Message):

    def __init__(self):
        super().__init__()

    def mount_message(self, topic_name):
        if (isinstance(topic_name, str)):
            self.packet['fixed_header'] = b'\xA2'
            packet_identifier = b'\x00' + b'\x01'
            #ver tamanho
            topic_name_size = b'\x00' + bytes(bytearray([len(topic_name)]))

            self.packet['variable_header'] = packet_identifier

            self.packet['payload'] = topic_name_size + \
                topic_name.encode('utf-8')

            remaining_size = self.get_remaining_size(
                len(self.packet['variable_header'] + self.packet['payload']))

            if(not remaining_size):
                self.packet = None
            else:
                self.packet['fixed_header'] = self.packet['fixed_header'] + \
                    remaining_size

    def parse_unsuback(self, unsuback):
        if(unsuback[0] == 176):
            return True
        else:
            print("Isn't unsuback\n")
            return False

from mqtt.messages.message import Message


class Subscribe(Message):

    def __init__(self):
        super().__init__()

    def mount_message(self, topic_name):
        if (isinstance(topic_name, str)):
            self.packet['fixed_header'] = b'\x82'
            packet_identifier = b'\x00' + b'\x00'
            qos = b'\x00'
            topic_name_size = b'\x00' + bytes(bytearray([len(topic_name)]))

            self.packet['variable_header'] = packet_identifier

            self.packet['payload'] = topic_name_size + \
                topic_name.encode('utf-8') + qos

            remaining_size = self.get_remaining_size(
                len(self.packet['variable_header'] + self.packet['payload']))
            self.packet['fixed_header'] = self.packet['fixed_header'] + \
                remaining_size

    def parse_suback(self, suback):
        if(suback[0] == 144):
            print("Pacote é um suback\n")
            if(suback[-1] == 0):
                print("Subscribe Aceito pelo broker\n")
                return 1
            else:
                print("Subscribe Rejeitado pelo broker\n")
                return 0
        else:
            print("Não é um suback\n")
            return 0

from mqtt.messages.message import Message


class Connect(Message):

    def __init__(self):
        super().__init__()

    def mount_message(self):
        protocol_name = b'\x00' + b'\x04' + "MQTT".encode('utf-8')
        protocol_level = b'\x04'
        flags = b'\x02'
        fixed_header_size = b'\x10'
        keep_alive = b'\x00' + b'\x00'
        # client id não setado
        client_id = b'\x00'

        self.packet['variable_header'] = protocol_name + \
            protocol_level + flags + keep_alive

        self.packet['payload'] = b'\x00' + \
            b'\x00' + client_id

        remaining_size = self.get_remaining_size(
            len(self.packet['variable_header'] + self.packet['payload']))

        if(not remaining_size):
            self.packet = None
        else:
            self.packet['fixed_header'] = fixed_header_size + remaining_size

    def parse_connack(self, connack):
        control = connack[0]
        if(control == 32):
            state = connack[3]
            if(state == 0):
                return True
            else:
                return False
        else:
            print("Isn't ConnAck\n")
            return False

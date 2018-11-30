from Message import Message


class Connect(Message):

    def __init__(self):
        super().__init__()

    def mount_message(self):
        protocol_name = b'\x00' + b'\x04' + "MQTT".encode('utf-8')
        protocol_level = b'\x04'
        flags = b'\x02'
        fixed_header_size = b'\x10'
        keep_alive = b'\x00' + b'\x00'
        # de onde vem esse client_id
        client_id = "JHL-001".encode('utf-8')

        self.packet['variable_header'] = protocol_name + \
            protocol_level + flags + keep_alive

        self.packet['payload'] = b'\x00' + \
            bytes(bytearray([len(client_id)])) + client_id

        remaining_size = self.get_remaining_size(
            len(self.packet['variable_header'] + self.packet['payload']))
        self.packet['fixed_header'] = fixed_header_size + remaining_size

    # Why dont use booleans and exceptions instead of integers?
    def parse_connack(self, connack):
        control = connack[0]
        print("Controle:", control)
        if(control == 32):
            state = connack[3]
            print("Estado:", state)
            if(state == 0):
                print("Conexão Aceita pelo Broker\n")
                return 1
            else:
                print("Conexão Recusada\n")
                return 0
        else:
            print("Não é um packet ConnAck\n")
            return 0

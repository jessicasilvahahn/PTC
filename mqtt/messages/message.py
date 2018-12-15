class Message:
    packet = {}

    def __init__(self):
        # estrutura de um packet mqtt
        self.packet = {
            'fixed_header': None,
            'variable_header': None,
            'payload': None
        }

    def get_complete_packet(self):
        if(self.packet['fixed_header'] == None or
                self.packet['variable_header'] == None or
                self.packet['payload'] == None or self.packet==None):
            print("Packet is incomplete or empty\n")
            return False
        else:
            return self.packet['fixed_header'] + \
                self.packet['variable_header'] + self.packet['payload']

    def get_remaining_size(self, tamanho):
        if(tamanho <= 127):
            remainingLength = []
            while(tamanho > 0):
                encodedByte = tamanho % 128
                tamanho = tamanho // 128
                if(tamanho > 0):
                    encodedByte = encodedByte | 128
                remainingLength.append(encodedByte)
            return bytes(remainingLength)
        else:
            print("Not allowed\n")
            print("Decrease topic size\n")
            return False

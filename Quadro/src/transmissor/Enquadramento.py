import serial

toInt = lambda hex: int.from_bytes(hex, byteorder='big')

class Enquadramento:
    def __init__(self,portaSerial,baud):
        self._serial = serial.Serial(portaSerial, baudrate=baud)
        self._serial.port = portaSerial
        self.n = None
        self.max_bytes = 256
        self.quadro = []

    def enquadra(self, byte):
        if ((byte == toInt(b'\x7E')) or (byte == toInt(b'\x7D'))):
            self.quadro.append(toInt(b'\x7D'))
            self.quadro.append(byte ^ 20)

        else:
            self.quadro.append(byte)


    def transmite(self, payload):
        print("Inicinado...")
        self.quadro.append(toInt(b'\x7E'))
        for byte in payload:
            self.enquadra(byte)
        #self.quadro.append(toInt(b'\x7E'))
        print(bytearray(self.quadro))
        self._serial.write(bytearray(self.quadro))
        self.quadro = []

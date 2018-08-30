import serial
from PTC.Quadro.src import crc

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


    def transmite(self, info):
        print("Inicinado...")
        objeto_crc = crc.CRC16(info)
        payload = objeto_crc.gen_crc()
        self.quadro.append(toInt(b'\x7E'))
        for byte in payload:
            self.enquadra(byte)
        self.quadro.append(toInt(b'\x7E'))
        print("transmitindo:",bytearray(self.quadro))
        #teste
        self.quadro[1] = self.quadro[1] ^ 10
        print(bytearray(self.quadro))
        self._serial.write(bytearray(self.quadro))
        self.quadro = []

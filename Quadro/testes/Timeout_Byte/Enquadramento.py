import serial
import crc


def toInt(hex): return int.from_bytes(hex, byteorder='big')


class Enquadramento:
    def __init__(self, portaSerial, baud):
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
        # para fazer p crc antes
        payload_crc = bytearray(info)
        crc16 = crc.CRC16(payload_crc)
        info = crc16.gen_crc()
        self.quadro.append(toInt(b'\x7E'))
        for byte in info:
            self.enquadra(byte)
        #forçando o envio de um quadro incompleto para ocasionar timeout de byte
        #self.quadro.append(toInt(b'\x7E'))
        self._serial.write(bytearray(self.quadro))
        self.quadro = []

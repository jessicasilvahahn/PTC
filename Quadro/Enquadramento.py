import serial
import Estado

class Enquadramento:
    _serial,_bytes_min,bytes_max,_serialPorta,_buffer,estado,n_bytes,_baud = None
    #tamanho do buffer = 4096
    def __init__(self,serial,bytes_min,bytes_max,baud):

        self._serial = serial
        self._bytes_min = bytes_min
        self._bytes_max = bytes_max
        self._baud = baud

    #fazer o enquadramento de acordo com as flags e envia para a serial
    #def envia(self,buffer,bytes):

    def recebe(self,buffer):
        quadro = self.readSerial()
        if quadro==0:
            return 0
        else:
            return quadro


    def readSerial(self):
        # pegando dados da serial
        # criando objeto serial
        s = serial.Serial(256)
        # set info
        s.baudrate = self._baud
        s.port = self._serialPorta
        data = None
        # ler 256 bytes
        try:
            #ler 256 byte de forma de bloqueante (True)
            b = s.read(256,True)
            data = data + b
            return  data
        except ValueError:
            return 0

    #maquina de estado do receptor, fazer
    #def handle(self,estado):







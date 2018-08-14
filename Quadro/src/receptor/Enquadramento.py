import serial as Serial
import Estado

class Enquadramento:
    _serial = None
    # FIXME: (lucas) probably will not be /dev/ttyUSB0
    def __init__(self, portaSerial='/dev/ttyUSB0', baud):
        _serial = Serial.Serial(baudRate=baud)
        _serial.port = serialPort 

    #fazer o enquadramento de acordo com as flags e envia para a serial
    #def envia(self,buffer,bytes):

    def desenquadra():
        n = None
   		if (estado == 'ocioso'):
		    byte = _serial.read() 
            if (byte == b'\x7E'):
                n = 0
                estado = 'RX'
        if (estado == 'recepcao'):
		    byte = _serial.read() 
            if (byte == b'\x7D'):
                estado = ''                
            else:
                
                

    def recebe(self,buffer):
#        quadro = self.readSerial()
#        if (quadro == 0):
#            return 0
#        else:
#            return quadro
#
#
#    def readSerial(self):
#        # pegando dados da serial
#        # criando objeto serial
#        s = serial.Serial()
#        # set info
#        s.baudrate = self._baud
#        s.port = self._portaSerial
#        data = None
#        # ler 256 bytes
#        try:
#            #ler 256 byte de forma de bloqueante (True)
#            # FIXME: prabably should read byte by byte
#            b = s.read()
#            data = data + b
#            return  data
#        except ValueError:
#            print('Ocorreu um erro ao tentar ler a serial')
#            # should return a number here?
#            return 0
#
    #maquina de estado do receptor, fazer
    #def desenquadra(self, estado):







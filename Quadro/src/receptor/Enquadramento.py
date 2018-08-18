import serial as Serial
import Estado
import timer

class Enquadramento:
    _serial = None
    # FIXME: (lucas) probably will not be /dev/ttyUSB0
    def __init__(self, portaSerial='/dev/ttyUSB0', baud):
        _serial = Serial.Serial(baudRate=baud, timeout=10.0)
        _serial.port = serialPort 

    #fazer o enquadramento de acordo com as flags e envia para a serial
    #def envia(self,buffer,bytes):

    def desenquadra(self,estado):
        n = None
        max_bytes = 256

  	if (estado == 'ocioso'):
		byte = _serial.read() 
            	if (byte == b'\x7E'):
                	n = 0
                	estado = 'RX'
	        else:
	    		estado = 'ocioso'
        if (estado == 'RX'):
		byte = _serial.read() 
            	if (byte == b'\x7D'):
                	estado = 'escape'                
            	elif (byte == b'\x7E'):
			estado = 'RX'
		else: #depois inserir logica de timeout 
			n = n + 1
			estado = 'recepcao'
	if (estado == 'escape'):
		byte = _serial.read()
		if ((byte == b'\x7E') or (byte == b'\x7D'): # timeout _serial.interCharTimeout()
			_serial.flushInput()
			_serial.flushOutput()
			estado = 'ocioso'
		else:
			n = n + 1
                	estado = 'recepcao'
	if (estado == 'recepcao')
		byte = _serial.read()
		frame = bytearray()
		if (byte == b'\x7D'):
			estado = 'escape'
		if (byte == b'\x7E'):
			buff = frame
			estado = 'ocioso'
		else: 
			if (len(frame) <= max_bytes):
				frame.append(byte)
				n = n +1
				estado = 'recepcao'
			else: 
				print('overflow')
				_serial.flushInput()
				_serial.flushOutput()
				estado = 'ocioso'
                

    def recebe(self,buffer):
#        quadro = self.readSerial()
#        if (quadro == 0):
#            return 0
#        else:
#            return quadro
#
#







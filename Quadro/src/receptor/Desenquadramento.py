import serial

class Desenquadramento:
    _serial = None
    def __init__(self,portaSerial,baud):
        self._serial = serial.Serial(portaSerial,baudrate=baud)
        self._serial.port = portaSerial
        self.n = None
        self.max_bytes = 256
        self.frame = []

    def desenquadra(self,estado,byte):
        buff = None
        if estado=="ocioso":
            print(estado)
            if byte == b'\x7E':
                self.n = 0
                estado = "rx"
            else:
                estado = "ocioso"
        if estado == "rx":
            print(estado)
            if byte==b'\x7D':
                estado = "escape"
            elif byte==b'\x7E':
                estado = "rx"
            else:
                self.n = self.n+1
                estado = "recepcao"
        if estado=="escape":
            print(estado)
            if byte==b'\x7E' or byte==b'\x7D':
                estado = "ocioso"
            else:
                self.n = self.n+1
                estado = "recepcao"

        if estado=="recepcao":
            print(estado)
            print(byte)
            if byte == b'\x7D':
                estado = "escape"
                return buff,estado
            if byte==b'\x7E':
                buff = self.frame
                estado = "ocioso"
            else:
                if len(self.frame) <= self.max_bytes:
                    self.n = self.n + 1
                    self.frame.append(byte)
                    estado = "recepcao"
                else:
                    print("overflow\n")
                    estado = "ocioso"
        return buff,estado




    def recebe(self):
        byte = self._serial.read()
        tamanhoBufferSerial = self._serial.inWaiting()
        return byte, tamanhoBufferSerial

#chamando maquina de estado

#inciando classe desenquadramento
d = Desenquadramento("/dev/pts/14",9600)
estado = "ocioso"
loop = 1

while loop:
    byte,tamanho = d.recebe()
    print(byte)
    loop = tamanho
    buff,estado = d.desenquadra(estado,byte)

print("Buffer recebido",buff,"\n")
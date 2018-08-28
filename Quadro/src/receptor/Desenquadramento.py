import serial

# TODO: Precisamos achar um nome melhor pra essa classe


class Desenquadrador:

    def __init__(self, portaSerial, baud):
        self.estado = "ocioso"
        self._serial = serial.Serial(port=portaSerial, baudrate=baud)
        self.n = None
        self.max_bytes = 256
        self.frame = []

    def desenquadra(self, byte):
        if self.estado == "ocioso":
            if byte == b'\x7E':
                self.iniciaRecepcao()
        if self.estado == "rx":
            if byte == b'\x7D':
                self.estado = "escape"
            elif byte == b'\x7E':
                self.estado = "rx"
            else:
                self.n = self.n + 1
                self.estado = "recepcao"
        if self.estado == "escape":
            if byte == b'\x7E' or byte == b'\x7D':
                self.finalizaRecepcao()
                mensagemErro = 'Recebeu byte de termino durante estado de escape'
                raise RuntimeError(mensagemErro)
            else:
                self.n = self.n + 1
                self.estado = "recepcao"

        if self.estado == "recepcao":
            if byte == b'\x7D':
                self.estado = "escape"
                return True
            if byte == b'\x7E':
                return False
            else:
                if self.n < self.max_bytes:
                    self.n = self.n + 1
                    self.frame.append(byte)
                    self.estado = "recepcao"
                else:
                    self.finalizaRecepcao()
                    erro = 'Excedeu o numero maximo de bytes em um pacote'
                    raise RuntimeError(erro)
        return True

    def iniciaRecepcao(self):
        self.n = 0
        self._serial.timeout = 3  # segundos
        self.estado = "rx"

    def finalizaRecepcao(self):
        self.estado = 'ocioso'
        self.n = None
        self.frame = []
        self._serial.timeout = None

    def recebe(self):
        continuarRecebendo = True
        while continuarRecebendo:
            byte = self._serial.read()
            if ((byte == b'') and (self.estado != "ocioso")):
                print("deu timeout")
                continuarRecebendo = False
            continuarRecebendo = self.desenquadra(byte)
        payload = self.frame
        self.finalizaRecepcao()
        return payload


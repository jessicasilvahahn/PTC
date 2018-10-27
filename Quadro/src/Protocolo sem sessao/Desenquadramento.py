import serial
import crc

# TODO: Precisamos achar um nome melhor pra essa classe


class Desenquadrador:

    def __init__(self, portaSerial, baud):
        self.objeto_crc = crc.CRC16(b'')
        self.estado = "ocioso"
        self._serial = serial.Serial(port=portaSerial, baudrate=baud)
        self.n = None
        self.max_bytes = 256
        self.frame = []
        self.estado_anterior = None

    def desenquadra(self, byte):
        self.estado_anterior = self.estado
        if self.estado == "ocioso":
            if byte == b'\x7E':
                self.iniciaRecepcao()
                return True
        if self.estado == "rx":
            if byte == b'\x7D':
                self.estado = "escape"
                return True
            elif byte == b'\x7E':  # verificar isso
                self.estado = "rx"
            else:
                self.estado = "recepcao"
        if self.estado == "escape":
            if byte == b'\x7E' or byte == b'\x7D':
                self.finalizaRecepcao()
                mensagemErro = 'Recebeu byte de termino durante estado de escape'
                raise RuntimeError(mensagemErro)
            else:
                info_original = int.from_bytes(byte, byteorder='big') ^ 0x20
                self.armazenaDado(info_original.to_bytes(1, byteorder='big'))
                return True

        if self.estado == "recepcao":
            if byte == b'\x7D':
                self.estado = "escape"
                return True
            if byte == b'\x7E':
                return False
            else:
                if self.n < self.max_bytes:  # tem que tirar isso aqui
                    self.armazenaDado(byte)
                    return True
                else:
                    self.finalizaRecepcao()
                    erro = 'Excedeu o numero maximo de bytes em um pacote'
                    raise RuntimeError(erro)
        return False

    def armazenaDado(self, dado):
        self.n = self.n + 1
        self.frame.append(dado)
        self.estado = "recepcao"

    def iniciaRecepcao(self):
        self.n = 0
        self._serial.timeout = 0.05  # segundos
        self.estado = "rx"

    def finalizaRecepcao(self):
        self.estado = 'ocioso'
        self.n = None
        self.frame = []
        self._serial.timeout = None

    def recebe(self):
        continuarRecebendo = True
        self._serial.timeout = 10 # segundos
        while continuarRecebendo:
            byte = self._serial.read()
            if (byte == b''):
                print("Ocorreu timeout")
                self.finalizaRecepcao()
                continuarRecebendo = False
                return []
            continuarRecebendo = self.desenquadra(byte)

        payload = self.frame
        #print("payload", payload)
        fcs = payload
        vet = bytearray()
        for i in range(len(fcs)):
            vet = vet + fcs[i]  # teste do payload corrompido: + fcs[i]
        self.objeto_crc = crc.CRC16(vet)
        check = self.objeto_crc.check_crc()
        if check == True:
            print("Dados confiaveis")
            self.finalizaRecepcao()
            return payload
        else:
            erro_crc = "PAYLOAD CORROMPIDO"
            raise RuntimeError(erro_crc)

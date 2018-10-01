from Enquadramento import Enquadramento
from Desenquadramento import Desenquadrador


def toInt(hex): return int.from_bytes(hex, byteorder='big')


class Arq:
    def __init__(self, tratador_aplicacao, porta_receptor, porta_transmissor):
        self.estado = "comunicando"
        self.m = False
        self.n = False
        self.payload = None
        self.tratador_aplicacao = tratador_aplicacao
        self.quadro = {
            'payload': None,
            'sequencia': None,
            'tipo': None,
        }

        self.receptor = Desenquadrador(porta_receptor, 9600)
        self.transmissor = Enquadramento(porta_transmissor, 9600)

    # estruturas comportamentais ------------------------------------------------
    def comportamentoArq(self, evento):
        print(evento)
        if self.estado == "comunicando":
            if evento == 'envia payload':
                self.envia_dados()
                self.estado = "aguardandoAck"
                return
            if evento == 'quadro recebido':
                self.trata_recebimento()
                return
        if self.estado == "aguardandoAck":
            if evento == 'quadro recebido':
                if self.quadro['tipo'] == 'dados':
                    self.trata_recebimento()
                    return
                if self.quadro['tipo'] == 'confirmacao':
                    if self.quadro['sequencia'] == self.n:
                        self.n = not self.n
                        self.estado = "comunicando"
                    return

    def trata_recebimento(self):
        if self.quadro['sequencia'] == self.m:
            self.tratador_aplicacao(self.quadro['payload'])
            self.envia_confirmacao()
            self.m = not self.m
            self.estado = "aguardandoAck"
        elif self.quadro['sequencia'] == (not self.m):
            self.envia_confirmacao()
            self.estado = "comunicando"

    # estruturas de recepcao --------------------------------------------------
    def recebe(self):
        quadro = self.receptor.recebe()
        self.quadro['sequencia'] = self.extrai_sequencia(quadro)
        self.quadro['tipo'] = self.extrai_tipo(quadro)
        self.quadro['payload'] = self.extrai_payload(quadro)
        self.comportamentoArq('quadro recebido')

    def extrai_payload(self, quadro):
        payload = quadro[2:-2]
        return payload

    def extrai_sequencia(self, quadro):
        controle = quadro[0]
        teste = (toInt(controle) & toInt(b'\x04'))
        return (toInt(controle) & toInt(b'\x04')) == toInt(b'\x04')

    # Foi usado and ao inves de &, porque o python nao suporta esse operador.
    def extrai_tipo(self, quadro):
        controle = quadro[0]
        return 'confirmacao' if ((toInt(controle) & toInt(b'\x40')) == toInt(b'\x40')) else 'dados'

    # estruturas de envio ---------------------------------------------------

    def envia(self, payload):
        # Nós suportamos apenas UTF-8 no momento :D
        payload = self.converte_tipo(payload)
        self.payload = payload
        self.comportamentoArq('envia payload')
        self.recebe()

    def envia_dados(self):
        controle = b'\x00'
        if self.n:
            controle |= b'\x04'
        header = [toInt(controle), toInt(b'\x00'), toInt(b'\x00')]
        quadro = header + list(self.payload)
        self.transmissor.transmite(quadro)

    def envia_confirmacao(self):
        controle = b'\x40'
        if self.n:
            controle |= b'\x04'
        quadro = [controle, b'\x00', b'\x00']
        quadro_convertido = self.converte_tipo(quadro)
        self.transmissor.transmite(quadro_convertido)

    # Funcao para conversao de tipos do payload

    def converte_tipo(self, payload):
        if type(payload) == type(''):
            return bytes(payload, 'utf-8')
        elif type(payload) == type(b''):
            return payload
        elif type(payload) == type([]):
            vet = bytearray()
            for i in range(len(payload)):
                vet = vet + payload[i]
            byte = bytes(vet)
            return byte
        elif int(payload):
            return bytes([payload])

        else:
            raise ValueError(
                'Suportamos no momento apenas str, bytes ou inteiros')

from Enquadramento import Enquadramento
from Desenquadramento import Desenquadrador

toInt = lambda hex: int.from_bytes(hex, byteorder='big')

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
        return (controle & b'\x04') == b'\x04'

    def extrai_tipo(self, quadro):
        controle = quadro[0]
        return 'confirmacao' if ((controle & b'\x40') == b'\x40') else 'dados'


    # estruturas de envio ---------------------------------------------------
    def envia(self, payload):
        # Nós suportamos apenas UTF-8 no momento :D
        self.payload = bytes(payload, 'utf-8')
        self.comportamentoArq('envia payload')

    def envia_dados(self):
        #problema de conversao
        controle = b'\x00'
        payload_list = []
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
        self.transmissor.transmite(bytearray(quadro))

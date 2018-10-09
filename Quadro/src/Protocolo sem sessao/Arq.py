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
        self.tentativas = 0
        self.quadro = {
            'payload': None,
            'sequencia': None,
            'tipo': None,
        }

        try:
            self.receptor = Desenquadrador(porta_receptor, 9600)
            self.transmissor = Enquadramento(porta_transmissor, 9600)
        except IOError:
            print("Alguma porta serial não encontrada")

    # estruturas comportamentais ------------------------------------------------
    def comportamentoArq(self, evento):
        print("Evento",evento)
        print("Estado",self.estado)
        if self.estado == "comunicando":
            if evento == 'envia payload':
                print("tentando enviar")
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
                        self.tentativas = 0
                        self.n = not self.n
                        self.estado = "comunicando"
                    return
            if evento == 'envia payload':
                self.envia_dados()
                self.estado = "aguardandoAck"

    def trata_recebimento(self):
        if self.quadro['sequencia'] == self.m:
            self.tratador_aplicacao(self.quadro['payload'])
            self.envia_confirmacao()
            self.m = not self.m
            self.estado = "aguardandoAck"
        elif self.quadro['sequencia'] == (not self.m):
            self.envia_confirmacao()
            self.estado = "comunicando"

    def trata_timeout(self):
        self.tentativas += 1
        self.comportamentoArq('envia payload')
        if(self.recebe()==[]):
            return []

        # estruturas de recepcao --------------------------------------------------

    def recebe(self):
        quadro = self.receptor.recebe()
        print("Quadro Recebido no ARQ", quadro)
        if ((quadro == [])):
            if (self.tentativas == 3):
                return []
            if (self.payload != None):
                if(self.trata_timeout() == []):
                    return []
            else:
                return []
        if(quadro!=[]):
            self.quadro['sequencia'] = self.extrai_sequencia(quadro)
            self.quadro['tipo'] = self.extrai_tipo(quadro)
            self.quadro['payload'] = self.extrai_payload(quadro)
            self.payload = None
            self.comportamentoArq('quadro recebido')
        return

    def extrai_payload(self, quadro):
        payload = quadro[2:-2]
        return payload

    def extrai_sequencia(self, quadro):
        controle = quadro[0]
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
        if(self.recebe()==[]):
            return []

    def envia_dados(self):
        controle = b'\x00'
        if self.n:
            controle |= b'\x04'
        quadro = [toInt(controle)] + [toInt(b'\x00')] + list(self.payload)
        self.transmissor.transmite(quadro)

    def envia_confirmacao(self):
        print("Envia confirmacao")
        controle = b'\x40'
        if self.n:
            controle |= b'\x04'
        quadro = [controle, b'\x00'] #controle + proto
        quadro_convertido = self.converte_list(quadro)
        print("Quadro de confirmação enviado (ack)",quadro)
        self.transmissor.transmite(quadro_convertido)

    # Funcao para conversao de tipos do payload

    def converte_tipo(self, payload):
        if type(payload) == type(''):
            return bytes(payload, 'utf-8')
        elif type(payload) == type(b''):
            return payload
        elif (isinstance(payload,int)):
            return bytes([payload])

        else:
            raise ValueError(
                'Suportamos no momento apenas str, bytes ou inteiros')

    def converte_list(self,payload):
        if(type(payload) == type([])):
            vet = bytearray()
            for i in range(len(payload)):
                vet = vet + payload[i]
            byte = bytes(vet)
            return byte

from Enquadramento import Enquadramento
from Desenquadramento import Desenquadrador


def toInt(hex): return int.from_bytes(hex, byteorder='big')


class Arq:
    def __init__(self, tratador_aplicacao, porta_receptor, porta_transmissor):

        self.proto = None
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
        if self.estado == "comunicando":
            if evento == 'envia payload':
                self.envia_dados()
                self.estado = "aguardandoAck"
                return
            if evento == 'quadro recebido':
                print("recebeu quadro de dados")
                self.trata_recebimento()
                return
        if self.estado == "aguardandoAck":
            if evento == 'quadro recebido':
                if self.quadro['tipo'] == 'dados':
                    self.trata_recebimento()
                    return
                if self.quadro['tipo'] == 'confirmacao':
                    print("Recebi confirmacao")
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
            self.envia_confirmacao()
            self.m = not self.m
            self.estado = "aguardandoAck"

    def trata_timeout(self):
        self.tentativas += 1
        self.comportamentoArq('envia payload')
        if(self.recebe()==[]):
            return []

        # estruturas de recepcao --------------------------------------------------

    def recebe(self,quadro):
        if ((quadro == [])):
            if (self.tentativas == 3):
                return []
            if (self.payload != None):
                if(self.trata_timeout() == []):
                    return []
            else:
                return []
        if(quadro != []):
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
        return (toInt(controle) & toInt(b'\x08')) == toInt(b'\x08')

    def extrai_tipo(self, quadro):
        controle = quadro[0]
        return 'confirmacao' if ((toInt(controle) & toInt(b'\x80')) == toInt(b'\x80')) else 'dados'

    # estruturas de envio ---------------------------------------------------

    def envia(self, proto,payload):
        #conversao proto
        print("recebeu proto original da tun", proto)
        print("recebeu da tun algo: ",self.converte_proto(proto))
        # Nós suportamos apenas UTF-8 no momento :D
        payload = self.converte_tipo(payload)
        self.payload = payload
        self.comportamentoArq('envia payload')
        return

    def envia_dados(self):
        print("envia dados")
        if self.n:
            controle = b'\x08'
        else:
            controle = b'\x00'
        print("prot dados: ", self.proto)
        self.converte_proto(self.proto)
        quadro = [toInt(controle)] + [toInt(self.proto)] + list(self.payload)
        print("Quadro ARQ:",bytearray(quadro))
        self.transmissor.transmite(quadro)

    def envia_confirmacao(self):
        if self.m:
            controle = b'\x88'
        else:
            controle = b'\x80'
        controle = bytes(controle)
        self.converte_proto(self.proto)
        quadro = [controle, self.proto]
        quadro_convertido = self.converte_list(quadro)
        print("enviando confirmacao\n")
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
        print("convert list",payload)
        if(type(payload) == type([])):
            vet = bytearray()
            for i in range(len(payload)):
                vet = vet + payload[i]
            byte = bytes(vet)
            return byte
    
    def converte_proto(self,proto):
        if(proto==b'\x04' or proto==b'\x06'):
            self.proto = proto
        #ipv4
        if(proto==2048):
            self.proto = b'\x04'
        #ver ipv6
        if(proto==34525):
            self.proto = b'\x06'
        if(proto!=2048 and proto!=34525 and proto!=b'\x04' and proto!=b'\x06'):
            self.proto = b'\x00'
        
        



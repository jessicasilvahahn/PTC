from Sessao import Sessao

class Protocolo:
    def __init__(self,tratadorAplicacao, portaReceptor, portaTransmissor):
        self.tratadorAplicacao = tratadorAplicacao
        self.portaReceptor = portaReceptor
        self.portaTransmissor = portaTransmissor
        self.sessao = Sessao(self.tratadorAplicacao, self.portaReceptor, self.portaTransmissor)

    def conectar(self):
        self.sessao.conectar()

    def desconectar(self):
        self.sessao.desconectar()

    def envia(self,payload):
        self.sessao.enviar(payload)

    def recebe(self):
        self.sessao.receber()

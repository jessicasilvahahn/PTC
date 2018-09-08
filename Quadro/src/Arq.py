from PTC.Quadro.src.transmissor import Enquadramento
from PTC.Quadro.src.receptor import Desenquadramento

#quadro arq é o payload do enquadramento
class Arq:
    def __init__(self):
        self.estado = "comunicando"
        self.m = False
        self.n = False
        self.quadro_recebido = None
        self.payload = None


    def MefArq(self):

        if(self.estado == "comunicando"):
            if(self.payload):
                self.envia()
                self.estado = "aguardandoAck"
                return
            if(self.quadro_recebido):
                if(self.m == self.extrai_sequencia):
                self.extrai_payload()
                self.confirma()
                self.m = not self.m





    #montar quadro arq
    def envia(self):
        pass

    #envia ack
    def confirma(self):
        pass

    #extrai o payload do quadro
    def extrai_payload(self):
        pass

    #extrai sequencia do byte de controle do quadro arq
    def extrai_sequencia(self):
        pass
